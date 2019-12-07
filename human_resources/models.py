from django.db import models
from django.urls import reverse


class Employee(models.Model):
    """
    Employee model is responsible of keeping contact information of employee
    and nomina information.
    """

    NATIONALITY_CHOICES = [
        ('DO', 'DOMINICAN'),
        ('USA', 'AMERICAN'),
        ('VEN', 'VENEZUELAN'),
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
    nationality = models.CharField(max_length=3, choices=NATIONALITY_CHOICES, default='DO')
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

    def pay(self, hours_worked=88):
        if self.payment_method == "SALARY":
            return self.salary
        elif self.payment_method == "PER HOUR":
            return self.hourly * hours_worked
        else:
            return "ERROR"

    def pay_after_taxes(self, hours_worked=88):
        if self.payment_method == "SALARY":
            return self.salary - self.employee_deductions(self.salary)
        elif self.payment_method == "PER HOUR":
            subtotal = (hours_worked * self.hourly)
            return subtotal - self.employee_deductions(subtotal)
        else:
            return "ERROR"
