from decimal import Decimal

from django.db import models
from django.urls import reverse


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
    employee = models.ForeignKey('Employee', null=True, on_delete=models.SET_NULL, related_name="employee")

    # PAYROLL TAXES
    EMPLOYEE_TAX_SFS = .0304
    EMPLOYEE_TAX_AFP = .0287
    EMPLOYEE_TOTAL_TAXES = EMPLOYEE_TAX_SFS + EMPLOYEE_TAX_AFP
    SFS_EMPLOYER_LIABILITY = .0709
    AFP_EMPLOYER_LIABILITY = .0710
    SRL_EMPLOYER_LIABILITY = .0110
    INFOTEP_EMPLOYER_LIABILITY = .01
    TOTAL_EMPLOYER_LIABILITIES = SFS_EMPLOYER_LIABILITY + AFP_EMPLOYER_LIABILITY + SRL_EMPLOYER_LIABILITY + INFOTEP_EMPLOYER_LIABILITY

    # RULES
    HORAS_EXTRAS_RATE = 1.35
    HORAS_FERIADOS_RATE = 2.00
    SALARY_TO_DAILY_DIV = 23.83

    normal_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    extra_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    feriado_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def quincena(self):
        if self.employee.payment_method == "SALARIO":
            return self.employee.salary / 2
        elif self.employee.payment_method == "POR HORA":
            return self.gross()
        else:
            return "ERROR"

    def salary_to_hourly(self):
        if self.employee.payment_method == "SALARIO":
            per_day = float(self.employee.salary) / self.SALARY_TO_DAILY_DIV
            return round((per_day / 8), 4)
        else:
            return "ERROR: EMPLOYEE NOT SALARY EMPLOYEE"

    def gross(self):
        if self.employee.payment_method == "SALARIO":
            extra_pay = self.salary_to_hourly() * float(self.extra_hours) * self.HORAS_EXTRAS_RATE
            feriado_pay = self.salary_to_hourly() * float(self.feriado_hours) * self.HORAS_FERIADOS_RATE
            return round((float(self.quincena()) + extra_pay + feriado_pay), 2)
        elif self.employee.payment_method == "POR HORA":
            extra_pay = self.extra_hours * Decimal(self.HORAS_EXTRAS_RATE) * self.employee.hourly
            feriado_pay = self.feriado_hours * self.employee.hourly * Decimal(self.HORAS_FERIADOS_RATE)
            amount = ((self.normal_hours * self.employee.hourly) + extra_pay + feriado_pay)
            return round(amount, 2)
        else:
            return "ERROR"

    def taxable_income(self):
        if self.employee.payment_method == "SALARIO":
            return self.quincena()
        elif self.employee.payment_method == "POR HORA":
            return (self.normal_hours * self.employee.hourly)
        else:
            return "ERROR"

    def netpay(self):
        if self.employee.nationality == "DOMINICAN":
            if self.employee.payment_method == "SALARIO":
                deductions = float(self.quincena()) * self.EMPLOYEE_TOTAL_TAXES
                return round((float(self.quincena()) - deductions), 2)
            elif self.employee.payment_method == "POR HORA":
                deductions = self.employee.hourly * self.normal_hours * Decimal(self.EMPLOYEE_TOTAL_TAXES)
                return round((self.gross() - deductions), 2)
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
            return self.EMPLOYEE_TAX_SFS * float(self.taxable_income())
        else:
            return "N/A"

    def AFP_employee_deduction(self):
        if self.employee.nationality == "DOMINICAN":
            return float(self.taxable_income()) * self.EMPLOYEE_TAX_AFP
        else:
            return "N/A"

    def SRL_employer_liability(self):
        if self.employee.nationality == "DOMINICAN":
            return self.taxable_income() * self.SRL_EMPLOYER_LIABILITY
        else:
            return "N/A"

    def AFP_employer_liability(self):
        if self.employee.nationality == "DOMINICAN":
            return self.taxable_income() * self.AFP_EMPLOYER_LIABILITY
        else:
            return "N/A"

    def SFS_employer_liability(self):
        if self.employee.nationality == "DOMINICAN":
            return self.taxable_income() * self.SFS_EMPLOYER_LIABILITY
        else:
            return "N/A"

    def INFOTEP_employer_liability(self):
        if self.employee.nationality == "DOMINICAN":
            return self.taxable_income() * self.INFOTEP_EMPLOYER_LIABILITY
        else:
            return "N/A"

    def total_employer_liabilities(self):
        if self.employee.nationality == "DOMINICAN":
            return self.taxable_income() * self.TOTAL_EMPLOYER_LIABILITIES
        else:
            return "N/A"
