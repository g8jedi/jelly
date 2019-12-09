from datetime import datetime
from random import randint

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

    def test_comprobante_salary_employee_netpay(self):
        payment_method = "SALARIO"
        SFS_tax = .0304
        AFP_tax = .0287
        salary = 15000
        deductions = (SFS_tax + AFP_tax) * salary
        employee_netpay = salary - deductions

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            salary=salary, payment_method=payment_method
        )
        comprobante = Comprobante.objects.create(employee=employee)

        self.assertAlmostEqual(comprobante.netpay(), employee_netpay)

    def test_comprobante_perhour_employee_netpay_normal_hours(self):
        payment_method = "POR HORA"
        SFS_tax = .0304
        AFP_tax = .0287
        hourly = 56
        normal_hours = randint(10, 88)
        deductions = (SFS_tax + AFP_tax) * (hourly * normal_hours)
        employee_netpay = (hourly * normal_hours) - deductions

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            hourly=hourly, payment_method=payment_method
        )
        comprobante = Comprobante.objects.create(employee=employee, normal_hours=normal_hours)

        self.assertAlmostEqual(comprobante.netpay(), employee_netpay)

    def test_comprobante_perhour_employee_netpay_with_extra_hours(self):
        payment_method = "POR HORA"
        SFS_tax = .0304
        AFP_tax = .0287
        hourly = 56
        HORAS_EXTRAS_RATE = 1.35
        normal_hours = randint(60, 88)
        extra_hours = randint(10, 88)
        subtotal = (hourly * HORAS_EXTRAS_RATE * extra_hours) + (hourly * normal_hours)
        deductions = (SFS_tax + AFP_tax) * (hourly * normal_hours)
        employee_netpay = subtotal - deductions

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            hourly=hourly, payment_method=payment_method
        )
        comprobante = Comprobante.objects.create(
            employee=employee, normal_hours=normal_hours, extra_hours=extra_hours
        )

        self.assertAlmostEqual(comprobante.netpay(), employee_netpay)

    def test_comprobante_salary_employee_net_pay_foreigner(self):
        payment_method = "SALARIO"
        salary = 15000
        nationality = "AMERICAN"

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            salary=salary, payment_method=payment_method, nationality=nationality
        )
        comprobante = Comprobante.objects.create(employee=employee)

        self.assertAlmostEqual(comprobante.netpay(), salary)

    def test_comprobante_porhora_employee_net_pay_foreigner(self):
        payment_method = "POR HORA"
        hourly = 56
        normal_hours = randint(60, 88)
        extra_hours = randint(10, 88)
        HORAS_EXTRAS_RATE = 1.35
        subtotal = (hourly * HORAS_EXTRAS_RATE * extra_hours) + (hourly * normal_hours)
        nationality = "AMERICAN"

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            hourly=hourly, payment_method=payment_method, nationality=nationality
        )
        comprobante = Comprobante.objects.create(
            employee=employee, normal_hours=normal_hours, extra_hours=extra_hours
        )

        self.assertAlmostEqual(comprobante.netpay(), subtotal)

    def test_comprobante_SFS_employee_deductions_salary(self):
        payment_method = "SALARIO"
        salary = 15000
        SFS_tax_rate = .0304
        SFS_employee_deductions = salary * SFS_tax_rate

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            salary=salary, payment_method=payment_method
        )
        comprobante = Comprobante.objects.create(employee=employee)

        self.assertAlmostEqual(comprobante.SFS_employee_deduction(), SFS_employee_deductions)

    def test_comprobante_AFP_employee_deductions_salary(self):
        payment_method = "SALARIO"
        salary = 15000
        AFP_tax_rate = .0287
        AFP_employee_deductions = salary * AFP_tax_rate

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            salary=salary, payment_method=payment_method
        )
        comprobante = Comprobante.objects.create(employee=employee)

        self.assertAlmostEqual(comprobante.AFP_employee_deduction(), AFP_employee_deductions)

    def test_comprobante_perhour_employee_deductions_with_extra_hours(self):
        payment_method = "POR HORA"
        SFS_tax = .0304
        AFP_tax = .0287
        hourly = 56
        HORAS_EXTRAS_RATE = 1.35
        normal_hours = randint(60, 88)
        extra_hours = randint(10, 88)
        subtotal = (hourly * HORAS_EXTRAS_RATE * extra_hours) + (hourly * normal_hours)
        deductions = (SFS_tax + AFP_tax) * (hourly * normal_hours)
        employee_netpay = subtotal - deductions

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            hourly=hourly, payment_method=payment_method
        )
        comprobante = Comprobante.objects.create(
            employee=employee, normal_hours=normal_hours, extra_hours=extra_hours
        )

        self.assertAlmostEqual(
            (comprobante.AFP_employee_deduction() + comprobante.SFS_employee_deduction()),
            deductions
        )

    def test_comprobante_salary_employee_with_hours_extra(self):
        payment_method = "SALARIO"
        salary = 18000
        HORAS_EXTRAS_RATE = 1.35
        SALARY_TO_DAILY_DIV = 23.83
        extra_hours = randint(10, 88)
        extra_pay = (salary / SALARY_TO_DAILY_DIV / 8) * extra_hours * HORAS_EXTRAS_RATE
        subtotal = extra_pay + salary

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            salary=salary, payment_method=payment_method
        )
        comprobante = Comprobante.objects.create(employee=employee, extra_hours=extra_hours)

        self.assertAlmostEqual(comprobante.subtotal(), subtotal)

    def test_comprobante_salary_feriado_hours(self):
        payment_method = "SALARIO"
        salary = randint(10000, 24000)
        HORAS_FERIADOS_RATE = 2.00
        SALARY_TO_DAILY_DIV = 23.83
        feriado_hours = randint(1, 25)
        feriado_pay = (salary / SALARY_TO_DAILY_DIV / 8) * feriado_hours * HORAS_FERIADOS_RATE
        subtotal = feriado_pay + salary

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            salary=salary, payment_method=payment_method
        )
        comprobante = Comprobante.objects.create(employee=employee, feriado_hours=feriado_hours)

        self.assertAlmostEqual(comprobante.subtotal(), subtotal)

    def test_comprobante_hourly_feriado_hours(self):
        payment_method = "POR HORA"
        hourly = randint(56, 120)
        HORAS_FERIADOS_RATE = 2.00
        feriado_hours = randint(1, 25)
        normal_hours = randint(75, 88)
        feriado_pay = hourly * feriado_hours * HORAS_FERIADOS_RATE
        subtotal = feriado_pay + (normal_hours * hourly)

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            hourly=hourly, payment_method=payment_method
        )
        comprobante = Comprobante.objects.create(employee=employee, normal_hours=normal_hours, feriado_hours=feriado_hours)

        self.assertAlmostEqual(comprobante.subtotal(), subtotal)

    def test_comprobante_SRL_employer_liability_salary(self):
        payment_method = "SALARIO"
        salary = randint(10000, 18000)
        SRL_EMPLOYER_LIABILITY = .0110
        SRL_employer_cost = salary * SRL_EMPLOYER_LIABILITY

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            salary=salary, payment_method=payment_method
        )
        comprobante = Comprobante.objects.create(employee=employee)

        self.assertAlmostEqual(comprobante.SRL_employer_liability(), SRL_employer_cost)
