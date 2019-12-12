from datetime import datetime
from decimal import Decimal
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
        salary = randint(10000, 30000)
        quincena = salary / 2
        deductions = (SFS_tax + AFP_tax) * quincena
        employee_netpay = quincena - deductions

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            salary=salary, payment_method=payment_method
        )
        comprobante = Comprobante.objects.create(employee=employee)

        self.assertAlmostEqual(comprobante.netpay(), round(employee_netpay, 2))

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

        self.assertAlmostEqual(comprobante.netpay(), Decimal(round(employee_netpay, 2)))

    def test_comprobante_perhour_employee_netpay_with_extra_hours(self):
        payment_method = "POR HORA"
        SFS_tax = .0304
        AFP_tax = .0287
        hourly = 56
        HORAS_EXTRAS_RATE = 1.35
        normal_hours = randint(60, 88)
        extra_hours = randint(10, 88)
        gross = (hourly * HORAS_EXTRAS_RATE * extra_hours) + (hourly * normal_hours)
        deductions = (SFS_tax + AFP_tax) * (hourly * normal_hours)
        employee_netpay = gross - deductions

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            hourly=hourly, payment_method=payment_method
        )
        comprobante = Comprobante.objects.create(
            employee=employee, normal_hours=normal_hours, extra_hours=extra_hours
        )

        self.assertAlmostEqual(comprobante.netpay(), Decimal(round(employee_netpay, 2)))

    def test_comprobante_salary_employee_netpay_foreigner(self):
        payment_method = "SALARIO"
        salary = randint(10000, 30000)
        quincena = salary / 2
        nationality = "AMERICAN"

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            salary=salary, payment_method=payment_method, nationality=nationality
        )
        comprobante = Comprobante.objects.create(employee=employee)

        self.assertAlmostEqual(comprobante.netpay(), round(quincena, 2))

    def test_comprobante_porhora_employee_net_pay_foreigner(self):
        payment_method = "POR HORA"
        hourly = 56
        normal_hours = randint(60, 88)
        extra_hours = randint(10, 88)
        HORAS_EXTRAS_RATE = 1.35
        gross = (hourly * HORAS_EXTRAS_RATE * extra_hours) + (hourly * normal_hours)
        nationality = "AMERICAN"

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            hourly=hourly, payment_method=payment_method, nationality=nationality
        )
        comprobante = Comprobante.objects.create(
            employee=employee, normal_hours=normal_hours, extra_hours=extra_hours
        )

        self.assertAlmostEqual(comprobante.netpay(), Decimal(round(gross, 2)))

    def test_comprobante_SFS_employee_deductions_salary(self):
        payment_method = "SALARIO"
        salary = randint(10000, 30000)
        quincena = salary / 2
        SFS_tax_rate = .0304
        SFS_employee_deductions = quincena * SFS_tax_rate

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            salary=salary, payment_method=payment_method
        )
        comprobante = Comprobante.objects.create(employee=employee)

        self.assertAlmostEqual(comprobante.SFS_employee_deduction(), SFS_employee_deductions)

    def test_comprobante_AFP_employee_deductions_salary(self):
        payment_method = "SALARIO"
        salary = randint(10000, 30000)
        quincena = salary / 2
        AFP_tax_rate = .0287
        AFP_employee_deductions = quincena * AFP_tax_rate

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
        gross = (hourly * HORAS_EXTRAS_RATE * extra_hours) + (hourly * normal_hours)
        deductions = (SFS_tax + AFP_tax) * (hourly * normal_hours)
        employee_netpay = gross - deductions

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
        salary = randint(10000, 24000)
        quincena = salary / 2
        HORAS_EXTRAS_RATE = 1.35
        SALARY_TO_DAILY_DIV = 23.83
        extra_hours = randint(10, 88)
        extra_pay = (salary / SALARY_TO_DAILY_DIV / 8) * extra_hours * HORAS_EXTRAS_RATE
        gross = extra_pay + quincena

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            salary=salary, payment_method=payment_method
        )
        comprobante = Comprobante.objects.create(employee=employee, extra_hours=extra_hours)

        self.assertAlmostEqual(comprobante.gross(), round(gross, 2))

    def test_comprobante_salary_feriado_hours(self):
        payment_method = "SALARIO"
        salary = randint(10000, 24000)
        quicena = salary / 2
        HORAS_FERIADOS_RATE = 2.00
        SALARY_TO_DAILY_DIV = 23.83
        feriado_hours = randint(1, 25)
        feriado_pay = (salary / SALARY_TO_DAILY_DIV / 8) * feriado_hours * HORAS_FERIADOS_RATE
        gross = feriado_pay + quicena

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            salary=salary, payment_method=payment_method
        )
        comprobante = Comprobante.objects.create(employee=employee, feriado_hours=feriado_hours)

        self.assertAlmostEqual(comprobante.gross(), round(gross, 2))

    def test_comprobante_hourly_feriado_hours(self):
        payment_method = "POR HORA"
        hourly = randint(56, 120)
        HORAS_FERIADOS_RATE = 2.00
        feriado_hours = randint(1, 25)
        normal_hours = randint(75, 88)
        feriado_pay = hourly * feriado_hours * HORAS_FERIADOS_RATE
        gross = feriado_pay + (normal_hours * hourly)

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            hourly=hourly, payment_method=payment_method
        )
        comprobante = Comprobante.objects.create(employee=employee, normal_hours=normal_hours, feriado_hours=feriado_hours)

        self.assertAlmostEqual(comprobante.gross(), gross)

    def test_comprobante_SRL_employer_liability_salary(self):
        payment_method = "SALARIO"
        salary = randint(10000, 18000)
        quicena = salary / 2
        SRL_EMPLOYER_LIABILITY = .0110
        SRL_employer_cost = quicena * SRL_EMPLOYER_LIABILITY

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            salary=salary, payment_method=payment_method
        )
        comprobante = Comprobante.objects.create(employee=employee)

        self.assertAlmostEqual(comprobante.SRL_employer_liability(), SRL_employer_cost)

    def test_comprobante_AFP_employer_liability_salary(self):
        payment_method = "SALARIO"
        salary = randint(10000, 18000)
        quincena  = salary / 2
        AFP_EMPLOYER_LIABILITY = .0710
        AFP_employer_cost = quincena * AFP_EMPLOYER_LIABILITY

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            salary=salary, payment_method=payment_method
        )
        comprobante = Comprobante.objects.create(employee=employee)

        self.assertAlmostEqual(comprobante.AFP_employer_liability(), AFP_employer_cost)

    def test_comprobante_SFS_employer_liability_salary(self):
        payment_method = "SALARIO"
        salary = randint(10000, 18000)
        quincena = salary / 2
        SFS_EMPLOYER_LIABILITY = .0709
        SFS_employer_cost = quincena * SFS_EMPLOYER_LIABILITY

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            salary=salary, payment_method=payment_method
        )
        comprobante = Comprobante.objects.create(employee=employee)

        self.assertAlmostEqual(comprobante.SFS_employer_liability(), SFS_employer_cost)

    def test_comprobante_INFOTEP_employer_liability_salary(self):
        payment_method = "SALARIO"
        salary = randint(10000, 18000)
        quincena = salary / 2
        INFOTEP_EMPLOYER_LIABILITY = .01
        INFOTEP_employer_cost = quincena * INFOTEP_EMPLOYER_LIABILITY

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            salary=salary, payment_method=payment_method
        )
        comprobante = Comprobante.objects.create(employee=employee)

        self.assertAlmostEqual(comprobante.INFOTEP_employer_liability(), INFOTEP_employer_cost)

    def test_comprobante_employer_liabilities_hourly(self):
        payment_method = "POR HORA"
        hourly = randint(56, 110)
        normal_hours = randint(56, 88)
        taxable_amount = hourly * normal_hours
        SFS_EMPLOYER_LIABILITY = .0709
        AFP_EMPLOYER_LIABILITY = .0710
        SRL_EMPLOYER_LIABILITY = .0110
        INFOTEP_EMPLOYER_LIABILITY = .01
        employer_cost = taxable_amount * (SFS_EMPLOYER_LIABILITY + AFP_EMPLOYER_LIABILITY + SRL_EMPLOYER_LIABILITY + INFOTEP_EMPLOYER_LIABILITY)

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            hourly=hourly, payment_method=payment_method
        )
        comprobante = Comprobante.objects.create(employee=employee, normal_hours=normal_hours)

        self.assertAlmostEqual(comprobante.total_employer_liabilities(), employer_cost)

    def test_comprobante_salary_employee_quincena(self):
        payment_method = "SALARIO"
        salary = 18000
        quincena = 18000 / 2

        employee = Employee.objects.create(
            forename="Ana", middle_name="Mariel", surname="Mercedes Acosta",
            hire_date=datetime.now(), date_of_birth=datetime.now(), gender="FEMALE",
            salary=salary, payment_method=payment_method
        )
        comprobante = Comprobante.objects.create(employee=employee)

        self.assertAlmostEquals(comprobante.quincena(), quincena)
