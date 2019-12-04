from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from human_resources.models import Employee


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
            hire_date=datetime.today(), date_of_birth=datetime.today()
        )

        url = reverse('human_resources:employee-detail', args=(employee.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
