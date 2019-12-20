from django.forms import ModelForm, DateInput
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *

from .models import Employee, Nomina, Comprobante


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


class ComprobanteForm(ModelForm):

    class Meta:
        model = Comprobante
        exclude = ()


ComprobanteFormSet = inlineformset_factory(
    Nomina, Comprobante, form=ComprobanteForm,
    fields=['employee', 'normal_hours', 'extra_hours', 'feriado_hours'], extra=0, can_delete=True
)


class NominaForm(ModelForm):
    class Meta:
        model = Nomina
        fields = [
            'pay_period_start', 'pay_period_end'
        ]
        widgets = {
            'pay_period_start': DateInput,
            'pay_period_end': DateInput
        }

    def __init__(self, *args, **kwargs):
        super(NominaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-3'
        self.helper.layout = Layout(
            Div(
                Field('pay_period_start'),
                Field('pay_period_end'),
                Fieldset('Select Employees',
                         Formset('employees')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Process')),
            )
        )
