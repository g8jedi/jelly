from django.test import TestCase

from nomina.models import Impuesto


class ImpuestoModelTest(TestCase):
    def test_impuesto_creation(self):
        title = "Seguro Familiar De Salud"
        short_name = "SFS"
        liable = "EMPLOYEE"
        tax_rate = 0.034
        due_day = 3

        impuesto = Impuesto.objects.create(
            title=title, short_name=short_name, liable=liable,
            tax_rate=tax_rate, due_date=due_day
        )

        self.assertIs(impuesto.title, title)
        self.assertIs(impuesto.short_name, short_name)
        self.assertIs(impuesto.liable, liable)
        self.assertIs(impuesto.tax_rate, tax_rate)
        self.assertIs(impuesto.due_date, due_day)
