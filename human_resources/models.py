from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save

import human_resources.labor_rules as Rule


class Employee(models.Model):
    """
    Employee model is responsible of keeping contact information of employee
    and nomina information.
    """

    NATIONALITY_CHOICES = [
        ('DOMINICAN', 'DOMINICAN'),
        ('AMERICAN', 'AMERICAN'),
        ('VENEZUELAN', 'VENEZUELAN'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('SALARIO', 'SALARIO'),
        ('POR HORA', 'POR HORA'),
    ]

    GENDER_CHOICES = [
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
    ]

    # Personal Information
    forename = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25, blank=True)
    surname = models.CharField(max_length=50)
    identification = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=10, choices=NATIONALITY_CHOICES, default='DOMINICAN')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)

    # Contact Information
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=12, blank=True)

    #  Job Related Information
    hire_date = models.DateField()
    active = models.BooleanField(default=True)
    payment_method = models.CharField(max_length=8, choices=PAYMENT_METHOD_CHOICES, default='SALARIO')
    salary = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    hourly = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('human_resources:employee-detail', args=(self.id,))

    def full_name(self):
        if self.middle_name == "":
            return self.forename + " " + self.surname
        else:
            return self.forename + " " + self.middle_name + " " + self.surname

    def __str__(self):
        return self.full_name()


class Comprobante(models.Model):
    """
    This model represents a paystub
    """
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name="employee")
    nomina = models.ForeignKey('Nomina', on_delete=models.CASCADE)
    normal_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    extra_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    feriado_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def quincena(self):
        if self.employee.payment_method == "SALARIO":
            return Decimal(self.employee.salary / 2)
        elif self.employee.payment_method == "POR HORA":
            return self.taxable_income()
        else:
            return "ERROR"

    def extra_hours_hourly(self):
        if self.employee.payment_method == "SALARIO":
            return round((self.salary_to_hourly() * Rule.HORAS_EXTRAS_RATE), 2)
        elif self.employee.payment_method == "POR HORA":
            return round((self.employee.hourly * Rule.HORAS_EXTRAS_RATE), 2)
        else:
            return "ERROR"

    def feriado_hours_hourly(self):
        if self.employee.payment_method == "SALARIO":
            return round((self.salary_to_hourly() * Rule.HORAS_FERIADOS_RATE), 2)
        elif self.employee.payment_method == "POR HORA":
            return round((self.employee.hourly * Rule.HORAS_FERIADOS_RATE), 2)
        else:
            return "ERROR"

    def salary_to_hourly(self):
        if self.employee.payment_method == "SALARIO":
            return round((self.employee.salary / Rule.SALARY_TO_DAILY_DIV / 8), 2)
        else:
            return "ERROR: EMPLOYEE NOT SALARY EMPLOYEE"

    def gross(self):
        if self.employee.payment_method == "SALARIO":
            extra_pay = self.extra_hours_income()
            feriado_pay = self.feriado_hours_income()
            return self.quincena() + extra_pay + feriado_pay
        elif self.employee.payment_method == "POR HORA":
            extra_pay = self.extra_hours_income()
            feriado_pay = self.feriado_hours_income()
            amount = round(((self.normal_hours * self.employee.hourly) + extra_pay + feriado_pay), 2)
            return amount
        else:
            return "ERROR"

    def taxable_income(self):
        if self.employee.payment_method == "SALARIO":
            return self.quincena()
        elif self.employee.payment_method == "POR HORA":
            return round((self.normal_hours * self.employee.hourly), 2)
        else:
            return "ERROR"

    def netpay(self):
        if self.employee.nationality == "DOMINICAN":
            if self.employee.payment_method == "SALARIO":
                return self.gross() - self.total_employee_deductions()
            elif self.employee.payment_method == "POR HORA":
                return self.gross() - self.total_employee_deductions()
        else:
            return self.gross()

    def SFS_employee_deduction(self):
        """
        Dominican Payroll Tax Rule:
        (SFS) Seguro Familiar De Salud
        The tax is imposed on both the employee 3.04% and employer 7.09%
        This method calculates the deductions to the employee off his salary or regular pay
        """
        if self.employee.nationality == "DOMINICAN":
            return round((Rule.EMPLOYEE_TAX_SFS * self.taxable_income()), 2)
        else:
            return "N/A"

    def AFP_employee_deduction(self):
        if self.employee.nationality == "DOMINICAN":
            return round((self.taxable_income() * Rule.EMPLOYEE_TAX_AFP), 2)
        else:
            return "N/A"

    def total_employee_deductions(self):
        if self.employee.nationality == "DOMINICAN":
            return self.SFS_employee_deduction() + self.AFP_employee_deduction()
        else:
            return "N/A"

    def SRL_employer_liability(self):
        if self.employee.nationality == "DOMINICAN":
            return round((self.taxable_income() * Rule.SRL_EMPLOYER_LIABILITY), 0)
        else:
            return "N/A"

    def AFP_employer_liability(self):
        if self.employee.nationality == "DOMINICAN":
            return round((self.taxable_income() * Rule.AFP_EMPLOYER_LIABILITY), 0)
        else:
            return "N/A"

    def SFS_employer_liability(self):
        if self.employee.nationality == "DOMINICAN":
            return round((self.taxable_income() * Rule.SFS_EMPLOYER_LIABILITY), 0)
        else:
            return "N/A"

    def INFOTEP_employer_liability(self):
        if self.employee.nationality == "DOMINICAN":
            return round((self.taxable_income() * Rule.INFOTEP_EMPLOYER_LIABILITY), 0)
        else:
            return "N/A"

    def extra_hours_income(self):
        if self.employee.payment_method == "SALARIO":
            return round((self.extra_hours_hourly() * self.extra_hours), 2)
        elif self.employee.payment_method == "POR HORA":
            return round((self.extra_hours * self.extra_hours_hourly()), 2)
        else:
            return "ERROR"

    def feriado_hours_income(self):
        if self.employee.payment_method == "SALARIO":
            return round((self.feriado_hours_hourly() * self.feriado_hours), 2)
        elif self.employee.payment_method == "POR HORA":
            return round((self.feriado_hours_hourly() * self.feriado_hours), 2)
        else:
            return "ERROR"


class Nomina(models.Model):
    """
    Model represents a pay period
    """
    complete = models.BooleanField(default=False)
    pay_period_start = models.DateField()
    pay_period_end = models.DateField()
    employees = models.ManyToManyField(Employee, limit_choices_to={'active': True})

    def pay_period(self):
        return "{} - {}".format(self.pay_period_start, self.pay_period_end)

    def __str__(self):
        return self.pay_period()

    def total_netpay(self):
        netpay = Decimal()
        comprobantes = self.comprobante_set.all()
        for comprobante in comprobantes:
            netpay += comprobante.netpay()
        return netpay


def set_up_nomina(sender, instance, **kwargs):
    if instance.employees.exists() is not True:
        active_employees = list(Employee.objects.filter(active=True))
        for employee in active_employees:
            instance.employees.add(employee)
            Comprobante.objects.create(nomina=instance, employee=employee)


post_save.connect(set_up_nomina, sender=Nomina)
