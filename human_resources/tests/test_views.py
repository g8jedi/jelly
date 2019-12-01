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
        self.assertContains(response, "forename")
        self.assertContains(response, "surname")
        self.assertContains(response, "identification")
        self.assertContains(response, "start_date")
