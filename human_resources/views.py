from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.forms import formset_factory
from django.template.loader import get_template
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
        return reverse_lazy('human_resources:comprobante-submit', kwargs={'pk': self.object.pk})


class NominaDetailView(generic.DetailView):
    model = Nomina


class ComprobanteSubmit(generic.UpdateView):
    model = Nomina
    template_name = 'human_resources/comprobante_create.html'
    form_class = NominaForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(ComprobanteSubmit, self).get_context_data(**kwargs)
        if self.request.POST:
            data['employees'] = ComprobanteFormSet(self.request.POST, instance=self.object)
        else:
            data['employees'] = ComprobanteFormSet(instance=self.object)
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
        return super(ComprobanteSubmit, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('human_resources:nomina-detail', kwargs={'pk': self.object.pk})


def send_email(request):
    """Email Send Test"""
    subject = "Email Received"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = ['jairo.batista21@gmail.com']
    contact_message = "Hello World!"

    send_mail(subject, contact_message, from_email, to_email, fail_silently=False)

    return render(request, 'human_resources/base.html')
