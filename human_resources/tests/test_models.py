from datetime import datetime

from django.test import TestCase
from django.utils import timezone

from human_resources.models import Employee, Comprobante


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
        payment_method = "SALARIO"
        salary = 15000
        employee = Employee.objects.create(
            forename=forename, middle_name=middle_name, surname=surname, identification=identification,
            hire_date=hire_date, date_of_birth=date_of_birth, active=active, email=email,
            payment_method=payment_method,phone_number=phone_number, nationality=nationality,
            gender=gender, salary=salary
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
        self.assertIs(employee.salary, salary)
        self.assertIs(employee.payment_method, payment_method)

    def test_employee_full_name_with_middle_name(self):
        forename = "Gianna"
        middle_name = "Y"
        surname = "Beato Batista"
        full_name = forename + " " + middle_name + " " + surname

        employee = Employee.objects.create(
            forename=forename, middle_name=middle_name, surname=surname,
            hire_date=datetime.now(), date_of_birth=datetime.now(),
            gender="FEMALE", salary=10000
        )

        self.assertEqual(employee.full_name(), full_name)

    def test_employee_full_name_no_middle_name(self):
        forename = "Gianna"
        surname = "Beato Batista"
        full_name = forename + " " + surname

        employee = Employee.objects.create(
            forename=forename, surname=surname,
            hire_date=datetime.now(), date_of_birth=datetime.now(),
            gender="FEMALE", salary=10000
        )

        self.assertEqual(employee.full_name(), full_name)

    def test_employee_pay_salary_method(self):
        payment_method = "SALARY"
        salary = 10000

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            salary=salary, payment_method=payment_method
        )

        self.assertIs(employee.pay(), salary)

    def test_employee_pay_hourly_method(self):
        payment_method = "PER HOUR"
        hourly = 56
        hours_worked = 44
        estimated_pay = hourly * hours_worked

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            hourly=hourly, payment_method=payment_method
        )

        self.assertAlmostEqual(employee.pay(hours_worked=hours_worked), estimated_pay)

    def test_pay_employee_salary_after_taxes(self):
        payment_method = "SALARY"
        salary = 10000
        SFS_tax = .0304
        AFP_tax = .0287
        deductions = (SFS_tax + AFP_tax) * salary
        pay_after_taxes = salary - deductions

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            salary=salary, payment_method=payment_method
        )

        self.assertAlmostEqual(employee.pay_after_taxes(), pay_after_taxes)

    def test_pay_employee_hourly_after_taxes(self):
        payment_method = "PER HOUR"
        hours_worked = 88
        hourly = 56
        SFS_tax = .0304
        AFP_tax = .0287
        subtotal = (hourly * hours_worked)
        deductions = (SFS_tax + AFP_tax) * subtotal
        pay_after_taxes = subtotal - deductions

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            hourly=hourly, payment_method=payment_method
        )

        self.assertAlmostEqual(employee.pay_after_taxes(), pay_after_taxes)


class ComprobanteModelTest(TestCase):
    def test_comprobante_creation(self):
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
        payment_method = "SALARIO"
        salary = 15000
        employee = Employee.objects.create(
            forename=forename, middle_name=middle_name, surname=surname, identification=identification,
            hire_date=hire_date, date_of_birth=date_of_birth, active=active, email=email,
            payment_method=payment_method, phone_number=phone_number, nationality=nationality,
            gender=gender, salary=salary
        )

        comprobante = Comprobante.objects.create(employee=employee)

        self.assertIs(comprobante.employee.forename, forename)
        self.assertIs(comprobante.employee.middle_name, middle_name)
        self.assertIs(comprobante.employee.surname, surname)
        self.assertIs(comprobante.employee.identification, identification)
        self.assertIs(comprobante.employee.date_of_birth, date_of_birth)
        self.assertIs(comprobante.employee.nationality, nationality)
        self.assertIs(comprobante.employee.email, email)
        self.assertIs(comprobante.employee.phone_number, phone_number)
        self.assertIs(comprobante.employee.gender, gender)
        self.assertIs(comprobante.employee.salary, salary)
        self.assertIs(comprobante.employee.payment_method, payment_method)