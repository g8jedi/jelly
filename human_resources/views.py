from django.shortcuts import render
from django.views import generic

from .models import Employee, Comprobante, Nomina
from .forms import EmployeeForm, NominaForm


class CreateEmployeeView(generic.edit.CreateView):
    """
    Create Employee Form
    """
    form_class = EmployeeForm
    model = Employee


class EmployeeDetailView(generic.DetailView):
    model = Employee


class EmployeeListView(generic.ListView):
    model = Employee


class ComprobanteDetailView(generic.DetailView):
    model = Comprobante


class CreateNominaView(generic.edit.CreateView):
    """
    Create Nomina Form
    """
    form_class = NominaForm
    model = Nomina