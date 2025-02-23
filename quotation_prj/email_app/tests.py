from django.test import TestCase, Client
from django.core import mail
from email_app.forms import UserMessageForm
from quotation_app.models import Client

#tests for the form
class UserMessageFormTest(TestCase):
    def test_valid_form(self):
        # Test valid data
        form_data = {
            'name': 'Joao da Silva',
            'email': 'joao@example.com',
        }
        form = UserMessageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Test invalid data (missing email)
        form_data = {
            'name': 'Joao da Silva',
            'email': '',  # Invalid: Email is required
        }
        form = UserMessageForm(data=form_data)
        self.assertFalse(form.is_valid())

#test for the view
""" class UserMessageViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_form_submission(self):
        # Test form submission
        response = self.client.post('/', {
            'name': 'Joao da Silva',
            'email': 'joao@example.com',
        })
        # Debugging: Print the response status code and content
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")

        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertRedirects(response, '/email_success/')

        # Check if the data was saved to the database
        self.assertEqual(UserMessage.objects.count(), 1)
        user_message = UserMessage.objects.first()
        self.assertEqual(user_message.name, 'Joao da Silva')
        self.assertEqual(user_message.email, 'joao@example.com')

        # Check if an email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Thank you for contacting us!')
        self.assertEqual(mail.outbox[0].to, ['joao@example.com']) """

""" class ClientModelTest(TestCase):
    def test_create_user_message(self):
        client = Client.objects.create(
            name='Alice',
            email='alice@example.com',
        )
        self.assertEqual(client.name, 'Alice')
        self.assertEqual(client.email, 'alice@example.com')
        self.assertIsNotNone(client.created_at)

class SuccessPageTest(TestCase):
    def test_success_page(self):
        client = Client()
        response = client.get('/success/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Thank you!') """