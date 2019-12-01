from django.test import TestCase
from django.utils import timezone

from human_resources.models import Employee


class EmployeeModelTests(TestCase):
    def test_employee(self):
        """
        Test if Employee can be instantiated.
        """
        forename = "Gianna"
        middle_name = "Haydee"
        surname = "Beato Batista"
        active = True
        start_date = timezone.now()
        identification = "230573204823"
        employee = Employee.objects.create(
            forename=forename, middle_name=middle_name, surname=surname,
            active=active, start_date=start_date, identification=identification
        )

        self.assertIs(employee.forename, forename)
        self.assertIs(employee.middle_name, middle_name)
        self.assertIs(employee.surname, surname)
        self.assertIs(employee.active, active)
        self.assertAlmostEquals(employee.start_date, start_date)
        self.assertIs(employee.identification, identification)

        #  2nd Iteration department, location, compesation: salary, hourly, etc...
