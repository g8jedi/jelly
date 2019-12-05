from django.db import models


class Impuesto(models.Model):
    """
    This Model accounts for payroll liability taxes for both employee and employer
    """
    LIABLE_CHOICES = [
        ('EMPLOYEE', 'EMPLOYEE'),
        ('COMPANY', 'COMPANY'),
    ]

    title = models.CharField(max_length=100)
    short_name = models.CharField(max_length=8)
    liable = models.CharField(max_length=10, choices=LIABLE_CHOICES, default='COMPANY')
    tax_rate = models.DecimalField(decimal_places=8, max_digits=10)
    due_date = models.IntegerField()
