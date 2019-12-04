from django.shortcuts import render
from django.views import generic

from .models import Employee
from .forms import EmployeeForm


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
