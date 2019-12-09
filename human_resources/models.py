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

    employee_tax_SFS = .0304
    employee_tax_AFP = .0287

    def employee_deductions(self, subtotal):
        """
        Helper method to calculate total deductions of employee taxes.
        """
        return (self.employee_tax_AFP + self.employee_tax_SFS) * subtotal

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

    def salary_to_hourly(self):
        if self.employee.payment_method == "SALARIO":
            return (self.employee.salary / self.SALARY_TO_DAILY_DIV / 8)
        else:
            return "ERROR: EMPLOYEE NOT SALARY EMPLOYEE"

    def subtotal(self):
        if self.employee.payment_method == "SALARIO":
            extra_pay = self.salary_to_hourly() * self.extra_hours * self.HORAS_EXTRAS_RATE
            feriado_pay = self.salary_to_hourly() * self.feriado_hours * self.HORAS_FERIADOS_RATE
            return self.employee.salary + extra_pay + feriado_pay
        elif self.employee.payment_method == "POR HORA":
            extra_pay = self.extra_hours * self.HORAS_EXTRAS_RATE * self.employee.hourly
            feriado_pay = self.feriado_hours * self.employee.hourly * self.HORAS_FERIADOS_RATE
            return (self.normal_hours * self.employee.hourly) + extra_pay + feriado_pay
        else:
            return "ERROR"

    def taxable_income(self):
        if self.employee.payment_method == "SALARIO":
            return self.employee.salary
        elif self.employee.payment_method == "POR HORA":
            return (self.normal_hours * self.employee.hourly)
        else:
            return "ERROR"

    def netpay(self):
        if self.employee.nationality == "DOMINICAN":
            if self.employee.payment_method == "SALARIO":
                deductions = self.employee.salary * self.EMPLOYEE_TOTAL_TAXES
                return self.employee.salary - deductions
            elif self.employee.payment_method == "POR HORA":
                deductions = self.employee.hourly * self.normal_hours * self.EMPLOYEE_TOTAL_TAXES
                return self.subtotal() - deductions
        else:
            return self.subtotal()

    def SFS_employee_deduction(self):
        """
        Dominican Payroll Tax Rule:
        (SFS) Seguro Familiar De Salud
        The tax is imposed on both the employee 3.04% and employer 7.09%
        This method calculates the deductions to the employee off his salary or regular pay
        """
        if self.employee.nationality == "DOMINICAN":
            return self.EMPLOYEE_TAX_SFS * self.taxable_income()
        else:
            return "N/A"

    def AFP_employee_deduction(self):
        if self.employee.nationality == "DOMINICAN":
            return self.taxable_income() * self.EMPLOYEE_TAX_AFP
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
