from django.forms import ModelForm, DateInput
from .models import Employee


class DateInput(DateInput):
    input_type = 'date'


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = [
            'forename', 'middle_name', 'surname', 'date_of_birth',
            'nationality', 'identification', 'gender',
            'email', 'phone_number', 'hire_date', 'salary',
        ]
        widgets = {
            'hire_date': DateInput,
            'date_of_birth': DateInput
        }
        labels = {
            'forename': ('Nombre'),
            'middle_name': ('Segundo nombre'),
            'surname': ('Apellidos'),
            'date_of_birth': ('Fecha de nacimiento'),
            'nationality': ('Nacionalidad'),
            'identification': ('Identificacion'),
            'gender': ('Sexo'),
            'phone_number': ('Whatsapp'),
            'hire_date': ('Fecha de contratación'),
            'salary': ('Salario'),

        }
