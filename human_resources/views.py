from django.db import transaction
from django.forms import formset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .models import Employee, Comprobante, Nomina
from .forms import EmployeeForm, NominaForm, ComprobanteForm, ComprobanteFormSet


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

    def get_success_url(self):
        return reverse_lazy('human_resources:nomina-detail', kwargs={'pk': self.object.pk})


class NominaDetailView(generic.DetailView):
    model = Nomina


class ComprobanteCreate(generic.CreateView):
    model = Comprobante
    template_name = 'human_resources/comprobante_create.html'
    form_class = NominaForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(ComprobanteCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['employees'] = ComprobanteFormSet(self.request.POST)
        else:
            data['employees'] = ComprobanteFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        employees = context['employees']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if employees.is_valid():
                employees.instance = self.object
                employees.save()
        return super(ComprobanteCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('human_resources:nomina-detail', kwargs={'pk': self.object.pk})
