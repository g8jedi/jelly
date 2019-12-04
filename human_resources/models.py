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

    GENDER_CHOICES = [
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
    ]

    # Personal Information
    forename = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25, blank=True, null=True)
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
    salary = models.DecimalField(max_digits=15, decimal_places=2, blank=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('human_resources:employee-detail', args=(self.id,))
