from django.db import models


class Employee(models.Model):
    """
    Employee class stores all information of an employee
    """
    forename = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25, null=True)
    surname = models.CharField(max_length=50)
    start_date = models.DateField()
    identification = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
