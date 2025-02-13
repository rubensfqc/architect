from django.test import TestCase, Client
from django.urls import reverse
from .models import Client as ClientModel, Quotation
from .forms import ClientForm, QuotationForm

# Models Tests
class ClientModelTest(TestCase):
    def test_create_client(self):
        client = ClientModel.objects.create(
            name="John Doe",
            email="john@example.com",
            whatsapp="12345678901"
        )
        self.assertEqual(client.name, "John Doe")
        self.assertEqual(client.email, "john@example.com")
        self.assertEqual(client.whatsapp, "12345678901")

class QuotationModelTest(TestCase):
    def test_create_quotation(self):
        client = ClientModel.objects.create(
            name="Jane Doe",
            email="jane@example.com",
            whatsapp="0987654321"
        )
        quotation = Quotation.objects.create(
            client=client,
            product_name="Product A",
            quantity=10,
            price=100.00
        )
        self.assertEqual(quotation.product_name, "Product A")
        self.assertEqual(quotation.quantity, 10)
        self.assertEqual(quotation.price, 100.00)
        self.assertEqual(quotation.total_price(), 1000.00)

# Forms Tests
class ClientFormTest(TestCase):
    def test_valid_client_form(self):
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'whatsapp': '12345678901'
        }
        form = ClientForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_client_form(self):
        data = {
            'name': '',
            'email': 'invalid-email',
            'whatsapp': ''
        }
        form = ClientForm(data=data)
        self.assertFalse(form.is_valid())

class QuotationFormTest(TestCase):
    def test_valid_quotation_form(self):
        data = {
            'product_name': 'Product A',
            'quantity': 10,
            'price': 100.00
        }
        form = QuotationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_quotation_form(self):
        data = {
            'product_name': '',
            'quantity': -5,
            'price': -100.00
        }
        form = QuotationForm(data=data)
        self.assertFalse(form.is_valid())

# Views Tests
class LandingPageViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_landing_page_get(self):
        response = self.client.get(reverse('landing_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quotation_app/landing_page.html')

    def test_landing_page_post(self):
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'whatsapp': '12345678901'
        }
        response = self.client.post(reverse('landing_page'), data=data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.assertTrue(ClientModel.objects.filter(name='John Doe').exists())

class QuotationPageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_client = ClientModel.objects.create(
            name='Jane Doe',
            email='jane@example.com',
            whatsapp='0987654321'
        )

    def test_quotation_page_get(self):
        response = self.client.get(reverse('quotation_page', args=[self.test_client.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quotation_app/quotation_page.html')

    def test_quotation_page_post(self):
        data = {
            'product_name': 'Product A',
            'quantity': 10,
            'price': 100.00
        }
        response = self.client.post(reverse('quotation_page', args=[self.test_client.id]), data=data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.assertTrue(Quotation.objects.filter(product_name='Product A').exists())

class GeneratePDFViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_client = ClientModel.objects.create(
            name='John Doe',
            email='john@example.com',
            whatsapp='12345678901'
        )
        self.test_quotation = Quotation.objects.create(
            client=self.test_client,
            product_name='Product A',
            quantity=10,
            price=100.00
        )

    def test_generate_pdf(self):
        response = self.client.get(reverse('generate_pdf', args=[self.test_quotation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment; filename=RFQ_John Doe.pdf', response['Content-Disposition'])