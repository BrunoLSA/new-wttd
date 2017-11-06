from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')
        self.form = self.resp.context['form']

    def test_get(self):
        """GET /inscricao/ must return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use template subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """Html must contain input tags"""
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit')

    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        #form = self.resp.context['form']
        self.assertIsInstance(self.form, SubscriptionForm)

    def test_form_has_fields(self):
        """form must have 4 fields: name, cpf, email, phone"""
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(self.form.fields))


class SubscribePostTest(TestCase):
    """Tests for valid posts"""
    def setUp(self):
        self.data = dict(name="Bruno Santana", cpf="12345678901",
                         email="santanasta@gmail.com", phone="92-99410-4333")
        self.resp = self.client.post('/inscricao/', self.data)
        self.email = mail.outbox[0]

    def test_post(self):
        """Valid POST should redirect to /inscricao/"""
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        """System must send email to user after subscription"""
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        """Email subject must be 'Confirmação de inscrição' """
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        """Email must be from santana@gmail.com"""
        expect = 'contato@eventex.com'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        """Email must be sent to the user and to the sender"""
        expect = ['contato@eventex.com', 'santanasta@gmail.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        """Email body must contain name, cpf, email and phone"""
        self.assertIn('Bruno Santana', self.email.body)
        self.assertIn('12345678901', self.email.body)
        self.assertIn('santanasta@gmail.com', self.email.body)
        self.assertIn('92-99410-4333', self.email.body)


class SubscribeInvalidPost(TestCase):
    """tests for invalid posts"""
    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})
        self.form = self.resp.context['form']

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        self.assertIsInstance(self.form, SubscriptionForm)

    def test_form_has_errors(self):
        self.assertTrue(self.form.errors)


class SubscribeSuccessMessage(TestCase):
    def setUp(self):
        self.data = dict(name="Bruno Santana", cpf="12345678901",
                         email="santanasta@gmail.com", phone="92-99410-4333")
        self.resp = self.client.post('/inscricao/', self.data, follow=True)

    def test_message(self):
        self.assertContains(self.resp, 'Inscrição realizada com sucesso!')