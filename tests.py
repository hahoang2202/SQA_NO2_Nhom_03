from django.test import TestCase
from .models import *
from .forms import *


class TestModels(TestCase):

    def setUp(self):
        self.client = Client.objects.create(
            meter_number=1234567,
            first_name='John',
            middle_name='Doe',
            last_name='Smith',
            contact_number='+639123456789',
            address='123 Main St., Anytown, USA',
            status='Connected'
        )

    def test_client_str(self):
        self.assertEqual(str(self.client), 'Smith, John Doe')

    def test_water_bill_payable_with_penalty(self):
        metric = Metric.objects.create(consump_amount=1, penalty_amount=2)
        bill = WaterBill.objects.create(
            name=self.client,
            meter_consumption=100,
            status='Pending',
            duedate=datetime.date.today(),
            penaltydate=datetime.date.today()
        )
        self.assertEqual(bill.payable(), 102)

class TestForms(TestCase):

    def test_bill_form_valid(self):
        form_data = {
            'name': Client.objects.create(
                meter_number=1234567,
                first_name='John',
                middle_name='Doe',
                last_name='Smith',
                contact_number='+639123456789',
                address='123 Main St., Anytown, USA',
                status='Connected'
            ).id,
            'meter_consumption': 100,
            'status': 'Pending',
            'duedate': datetime.date.today(),
            'penaltydate': datetime.date.today()
        }
        form = BillForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_client_form_valid(self):
        form_data = {
            'meter_number':1234567,
            'first_name': 'John',
            'middle_name': 'Doe',
            'last_name': 'Smith',
            'contact_number': '+639123456789',
            'address': '123 Main St., Anytown, USA',
            'status': 'Connected'
        }
        form = ClientForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_metrics_form_valid(self):
        form_data = {
            'consump_amount': 1,
            'penalty_amount': 2
        }
        form = MetricsForm(data=form_data)
        self.assertTrue(form.is_valid())

