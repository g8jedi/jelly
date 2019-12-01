from django.forms import ModelForm
from .models import Employee


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['forename', 'surname', 'middle_name', 'start_date', 'identification']
