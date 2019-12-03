from django.forms import ModelForm, DateInput
from .models import Employee


class DateInput(DateInput):
    input_type = 'date'


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['forename', 'middle_name', 'surname', 'identification', 'hire_date']
        widgets = {
            'hire_date': DateInput,
        }
        labels = {
            'forename': ('First Name'),
            'surname': ('Last Name'),
        }
