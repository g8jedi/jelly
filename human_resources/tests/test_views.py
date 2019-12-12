from datetime import datetime
from decimal import Decimal
from random import randint

from django.test import TestCase
from django.urls import reverse

from human_resources.models import Employee, Comprobante
import human_resources.labor_rules as Rules


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

    def test_comprobante_detail_correct_employee_details(self):
        forename = "Malcom"
        surname = "X"
        nationality = "AMERICAN"
        identification = "108801000"
        payment_method = "POR HORA"
        hourly = 67
        normal_hours = 88

        employee = Employee.objects.create(
            forename=forename, surname=surname, identification=identification,
            hire_date=datetime.today(), date_of_birth=datetime.today(),
            hourly=hourly, nationality=nationality, payment_method=payment_method,
        )
        comprobante = Comprobante.objects.create(employee=employee)
        url = reverse('human_resources:comprobante-detail', args=(comprobante.id,))
        response = self.client.get(url)

        self.assertContains(response, forename)
        self.assertContains(response, surname)
        self.assertContains(response, nationality)
        self.assertContains(response, identification)
        self.assertContains(response, payment_method)

    def test_comprobante_detail_salary_correct_quincena(self):
        forename = "Malcom"
        surname = "X"
        nationality = "AMERICAN"
        identification = "108801000"
        payment_method = "SALARIO"
        salary = 18000
        quincena = salary / 2

        employee = Employee.objects.create(
            forename=forename, surname=surname, identification=identification,
            hire_date=datetime.today(), date_of_birth=datetime.today(),
            salary=salary, nationality=nationality, payment_method=payment_method,
        )
        comprobante = Comprobante.objects.create(employee=employee)
        url = reverse('human_resources:comprobante-detail', args=(comprobante.id,))
        response = self.client.get(url)

        self.assertContains(response, quincena)

    def test_comprobante_detail_salary_horas_extras_info(self):
        forename = "Malcom"
        surname = "X"
        nationality = "AMERICAN"
        identification = "108801000"
        payment_method = "SALARIO"
        salary = randint(10000, 25000)
        extra_hours = randint(1, 35)
        salary_to_hourly = round((salary / Rules.SALARY_TO_DAILY_DIV / 8), 2)
        horas_extras_hourly = round((salary_to_hourly * Rules.HORAS_EXTRAS_RATE), 2)
        horas_extras_income = extra_hours * horas_extras_hourly

        employee = Employee.objects.create(
            forename=forename, surname=surname, identification=identification,
            hire_date=datetime.today(), date_of_birth=datetime.today(),
            salary=salary, nationality=nationality, payment_method=payment_method,
        )
        comprobante = Comprobante.objects.create(employee=employee, extra_hours=extra_hours)
        url = reverse('human_resources:comprobante-detail', args=(comprobante.id,))
        response = self.client.get(url)

        self.assertContains(response, horas_extras_income)
        self.assertContains(response, horas_extras_hourly)

    def test_comprobante_detail_salary_horas_feriados_info(self):
        forename = "Malcom"
        surname = "X"
        nationality = "AMERICAN"
        identification = "108801000"
        payment_method = "SALARIO"
        salary = randint(10000, 25000)
        feriado_hours = randint(1, 35)
        salary_to_hourly = round((salary / Rules.SALARY_TO_DAILY_DIV / 8), 2)
        horas_feriados_hourly = round((salary_to_hourly * Rules.HORAS_FERIADOS_RATE), 2)
        horas_feriados_income = horas_feriados_hourly * feriado_hours

        employee = Employee.objects.create(
            forename=forename, surname=surname, identification=identification,
            hire_date=datetime.today(), date_of_birth=datetime.today(),
            salary=salary, nationality=nationality, payment_method=payment_method,
        )
        comprobante = Comprobante.objects.create(employee=employee, feriado_hours=feriado_hours)
        url = reverse('human_resources:comprobante-detail', args=(comprobante.id,))
        response = self.client.get(url)

        self.assertContains(response, horas_feriados_income)
        self.assertContains(response, horas_feriados_hourly)

    def test_comprobante_detail_passport(self):
        nationality = "AMERICAN"
        employee = Employee.objects.create(
            forename="Malcolm", surname="X", identification="23523534",
            hire_date=datetime.today(), date_of_birth=datetime.today(),
            salary=213445, nationality=nationality, payment_method="SALARIO",
        )
        comprobante = Comprobante.objects.create(employee=employee)
        url = reverse('human_resources:comprobante-detail', args=(comprobante.id,))
        response = self.client.get(url)

        self.assertContains(response, "Passport")
        self.assertNotContains(response, "Cedula")
