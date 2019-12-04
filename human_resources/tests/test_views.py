from django.test import TestCase
from django.urls import reverse


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
