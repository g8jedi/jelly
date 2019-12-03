from datetime import datetime

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
        hire_date = datetime.now()
        active = True
        date_of_birth = datetime.now()
        email = "jairo@tacomoe.com"
        phone_number = "8097553433"
        nationality = "DOMINICAN"
        gender = "FEMALE"
        identification = "230573204823"
        employee = Employee.objects.create(
            forename=forename, middle_name=middle_name, surname=surname, identification=identification,
            hire_date=hire_date, date_of_birth=date_of_birth, active=active, email=email,
            phone_number=phone_number, nationality=nationality, gender=gender
        )

        self.assertIs(employee.forename, forename)
        self.assertIs(employee.middle_name, middle_name)
        self.assertIs(employee.surname, surname)
        self.assertIs(employee.identification, identification)
        self.assertIs(employee.hire_date, hire_date)
        self.assertIs(employee.date_of_birth, date_of_birth)
        self.assertIs(employee.nationality, nationality)
        self.assertIs(employee.active, active)
        self.assertIs(employee.email, email)
        self.assertIs(employee.phone_number, phone_number)
        self.assertIs(employee.gender, gender)

# 2nd Iteration department, location, compesation: salary, hourly, etc...
