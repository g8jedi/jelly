from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from human_resources.models import Employee, Comprobante


class EmployeeFormViewTests(TestCase):
    def test_employee_attribute_forms(self):
        """
        Test if Employee forms appear
        """
        url = reverse('human_resources:create-employee')
        response = self.client.get(url)

        # Test attribute descriptions appear
        self.assertContains(response, "Nombre")
        self.assertContains(response, "Apellido")
        self.assertContains(response, "Identificacion")
        self.assertContains(response, "Sexo")


class EmployeeDetailViewTests(TestCase):
    def test_employee_detail_view_200(self):
        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariela", surname="J", identification="341314", 
            hire_date=datetime.today(), date_of_birth=datetime.today(), salary=10000
        )

        url = reverse('human_resources:employee-detail', args=(employee.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class EmployeeListViewTests(TestCase):
    def test_employee_list_view_200(self):
        response = self.client.get(reverse('human_resources:employee-list'))
        self.assertEqual(response.status_code, 200)


class ComprobanteDetailViewTests(TestCase):
    def test_comprobante_detail_view_200(self):
        employee = Employee.objects.create(
            forename="John", middle_name="Gabe", surname="Doe", identification="341314", 
            hire_date=datetime.today(), date_of_birth=datetime.today(), salary=10000
        )
        comprobante = Comprobante.objects.create(employee=employee)
        url = reverse('human_resources:comprobante-detail', args=(comprobante.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)