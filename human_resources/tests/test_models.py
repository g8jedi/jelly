from datetime import datetime
from decimal import Decimal
from random import randint

from django.test import TestCase
from django.utils import timezone

from human_resources.models import Employee, Comprobante, Nomina
import human_resources.labor_rules as Rules


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
            payment_method=payment_method, phone_number=phone_number, nationality=nationality,
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

    def test_comprobante_salary_employee_dominican(self):
        # Employee Set Up
        nationality = "DOMINICAN"
        salary = randint(10200, 28000)
        quincena = Decimal(salary / 2)
        payment_method = "SALARIO"

        # Comprobante Logic
        extra_hours = randint(1, 25)
        feriado_hours = randint(3, 35)
        salary_to_hourly = round((salary / Rules.SALARY_TO_DAILY_DIV / 8), 2)
        extra_hours_hourly = round((salary_to_hourly * Rules.HORAS_EXTRAS_RATE), 2)
        feriado_hours_hourly = round((salary_to_hourly * Rules.HORAS_FERIADOS_RATE), 2)
        extra_hours_income = round((extra_hours * extra_hours_hourly), 2)
        feriado_hours_income = round((feriado_hours * feriado_hours_hourly), 2)
        gross = quincena + extra_hours_income + feriado_hours_income

        # Deductions
        taxable_income = quincena
        AFP_deduction = round((taxable_income * Rules.EMPLOYEE_TAX_AFP), 2)
        SFS_deduction = round((taxable_income * Rules.EMPLOYEE_TAX_SFS), 2)
        total_deductions = AFP_deduction + SFS_deduction
        net = gross - total_deductions

        employee = Employee.objects.create(
            forename="Jairo", surname="Batista", identification="235214214tewf",
            hire_date=datetime.now(), date_of_birth=datetime.now(),
            payment_method=payment_method, nationality=nationality,
            gender="MALE", salary=salary
        )

        comprobante = Comprobante.objects.create(employee=employee, extra_hours=extra_hours, feriado_hours=feriado_hours)

        self.assertEqual(comprobante.gross(), gross)
        self.assertEqual(comprobante.extra_hours_hourly(), extra_hours_hourly)
        self.assertEqual(comprobante.feriado_hours_hourly(), feriado_hours_hourly)
        self.assertEqual(comprobante.extra_hours_income(), extra_hours_income)
        self.assertEqual(comprobante.feriado_hours_income(), feriado_hours_income)
        self.assertEqual(comprobante.taxable_income(), taxable_income)
        self.assertEqual(comprobante.AFP_employee_deduction(), AFP_deduction)
        self.assertEqual(comprobante.SFS_employee_deduction(), SFS_deduction)
        self.assertEqual(comprobante.total_employee_deductions(), total_deductions)
        self.assertEqual(comprobante.netpay(), net)

    def test_comprobante_porhora_employee_dominican(self):
        # Employee Set Up
        nationality = "DOMINICAN"
        hourly = randint(56, 100)
        payment_method = "POR HORA"

        # Comprobante Logic
        normal_hours = randint(50, 88)
        extra_hours = randint(1, 25)
        feriado_hours = randint(3, 35)
        taxable_income = hourly * normal_hours
        extra_hours_hourly = round((hourly * Rules.HORAS_EXTRAS_RATE), 2)
        feriado_hours_hourly = round((hourly * Rules.HORAS_FERIADOS_RATE), 2)
        extra_hours_income = round((extra_hours * extra_hours_hourly), 2)
        feriado_hours_income = round((feriado_hours * feriado_hours_hourly), 2)
        gross = taxable_income + extra_hours_income + feriado_hours_income

        # Deductions
        AFP_deduction = round((taxable_income * Rules.EMPLOYEE_TAX_AFP), 2)
        SFS_deduction = round((taxable_income * Rules.EMPLOYEE_TAX_SFS), 2)
        total_deductions = AFP_deduction + SFS_deduction
        net = gross - total_deductions

        employee = Employee.objects.create(
            forename="Jairo", surname="Batista", identification="235214214tewf",
            hire_date=datetime.now(), date_of_birth=datetime.now(),
            payment_method=payment_method, nationality=nationality,
            gender="MALE", hourly=hourly
        )

        comprobante = Comprobante.objects.create(
            employee=employee, extra_hours=extra_hours, feriado_hours=feriado_hours, normal_hours=normal_hours
        )

        self.assertEqual(comprobante.gross(), gross)
        self.assertEqual(comprobante.extra_hours_hourly(), extra_hours_hourly)
        self.assertEqual(comprobante.feriado_hours_hourly(), feriado_hours_hourly)
        self.assertEqual(comprobante.extra_hours_income(), extra_hours_income)
        self.assertEqual(comprobante.feriado_hours_income(), feriado_hours_income)
        self.assertEqual(comprobante.taxable_income(), taxable_income)
        self.assertEqual(comprobante.AFP_employee_deduction(), AFP_deduction)
        self.assertEqual(comprobante.SFS_employee_deduction(), SFS_deduction)
        self.assertEqual(comprobante.total_employee_deductions(), total_deductions)
        self.assertEqual(comprobante.netpay(), net)
        self.assertEqual(comprobante.taxable_income(), taxable_income)

    def test_comprobante_porhora_employee_foreigner(self):
        # Employee Set Up
        nationality = "AMERICAN"
        hourly = randint(56, 100)
        payment_method = "POR HORA"

        # Comprobante Logic
        normal_hours = randint(50, 88)
        extra_hours = randint(1, 25)
        feriado_hours = randint(3, 35)
        taxable_income = hourly * normal_hours
        extra_hours_hourly = round((hourly * Rules.HORAS_EXTRAS_RATE), 2)
        feriado_hours_hourly = round((hourly * Rules.HORAS_FERIADOS_RATE), 2)
        extra_hours_income = round((extra_hours * extra_hours_hourly), 2)
        feriado_hours_income = round((feriado_hours * feriado_hours_hourly), 2)
        gross = taxable_income + extra_hours_income + feriado_hours_income

        employee = Employee.objects.create(
            forename="Jairo", surname="Batista", identification="235214214tewf",
            hire_date=datetime.now(), date_of_birth=datetime.now(),
            payment_method=payment_method, nationality=nationality,
            gender="MALE", hourly=hourly
        )

        comprobante = Comprobante.objects.create(
            employee=employee, extra_hours=extra_hours, feriado_hours=feriado_hours, normal_hours=normal_hours
        )

        self.assertEqual(comprobante.AFP_employee_deduction(), "N/A")
        self.assertEqual(comprobante.SFS_employee_deduction(), "N/A")
        self.assertEqual(comprobante.total_employee_deductions(), "N/A")
        self.assertEqual(comprobante.netpay(), gross)

    def test_comprobante_salary_employee_foreigner(self):
        # Employee Set Up
        nationality = "AMERICAN"
        salary = randint(10200, 28000)
        quincena = Decimal(salary / 2)
        payment_method = "SALARIO"

        # Comprobante Logic
        extra_hours = randint(1, 25)
        feriado_hours = randint(3, 35)
        salary_to_hourly = round((salary / Rules.SALARY_TO_DAILY_DIV / 8), 2)
        extra_hours_hourly = round((salary_to_hourly * Rules.HORAS_EXTRAS_RATE), 2)
        feriado_hours_hourly = round((salary_to_hourly * Rules.HORAS_FERIADOS_RATE), 2)
        extra_hours_income = round((extra_hours * extra_hours_hourly), 2)
        feriado_hours_income = round((feriado_hours * feriado_hours_hourly), 2)
        gross = quincena + extra_hours_income + feriado_hours_income

        employee = Employee.objects.create(
            forename="Jairo", surname="Batista", identification="235214214tewf",
            hire_date=datetime.now(), date_of_birth=datetime.now(),
            payment_method=payment_method, nationality=nationality,
            gender="MALE", salary=salary
        )

        comprobante = Comprobante.objects.create(employee=employee, extra_hours=extra_hours, feriado_hours=feriado_hours)

        self.assertEqual(comprobante.netpay(), comprobante.gross())
        self.assertEqual(comprobante.AFP_employee_deduction(), "N/A")
        self.assertEqual(comprobante.SFS_employee_deduction(), "N/A")
        self.assertEqual(comprobante.total_employee_deductions(), "N/A")


class NominaModelTest(TestCase):
    def test_nomina_instance(self):
        pay_period_start = datetime.now()
        pay_period_end = datetime.now()

        nomina = Nomina.objects.create(pay_period_start=pay_period_start, pay_period_end=pay_period_end)

        self.assertEqual(nomina.pay_period_start, pay_period_start)
        self.assertEqual(nomina.pay_period_end, pay_period_end)
