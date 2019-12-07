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
    employee_tax_ATP = .0287

    def employee_deductions(self, subtotal):
        """
        Helper method to calculate total deductions of employee taxes.
        """
        return (self.employee_tax_ATP + self.employee_tax_SFS) * subtotal

    # Personal Information
    forename = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25, blank=True)
    surname = models.CharField(max_length=50)
    identification = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=3, choices=NATIONALITY_CHOICES, default='DOMINICAN')
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


class Comprobante(models.Model):
    """
    This model represents a paystub
    """
    employee = models.ForeignKey('Employee', null=True, on_delete=models.SET_NULL, related_name="employee")

    # PAYROLL TAXES
    EMPLOYEE_TAX_SFS = .0304
    EMPLOYEE_TAX_ATP = .0287
    EMPLOYEE_TOTAL_TAXES = EMPLOYEE_TAX_SFS + EMPLOYEE_TAX_ATP
    EMPLOYER_TAX_SFS = .0709
    EMPLOYER_TAX_AFP = .0710
    EMPLOYER_TAX_SRL = .0110
    EMPLOYER_TOTAL_TAXES = EMPLOYER_TAX_AFP + EMPLOYER_TAX_SFS + EMPLOYER_TAX_SRL

    # RULES
    HORAS_EXTRAS_RATE = 1.35
    HORAS_FERIADOS_RATE = 2.00
    SALARY_TO_DAILY_DIV = 23.83

    normal_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    extra_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def subtotal(self):
        if self.employee.payment_method == "SALARIO":
            return self.employee.salary
        elif self.employee.payment_method == "POR HORA":
            return (self.normal_hours * self.employee.hourly) + (self.extra_hours * self.HORAS_EXTRAS_RATE * self.employee.hourly)
        else:
            return "ERROR"

    def netpay(self):
        if self.employee.nationality == "DOMINICAN":
            if self.employee.payment_method == "SALARIO":
                deductions = self.employee.salary * self.EMPLOYEE_TOTAL_TAXES
                return self.employee.salary - deductions
            elif self.employee.payment_method == "POR HORA":
                deductions = self.subtotal() * self.EMPLOYEE_TOTAL_TAXES
                return self.subtotal() - deductions
        else:
            return self.subtotal()
