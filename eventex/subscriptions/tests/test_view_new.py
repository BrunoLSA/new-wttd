from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscriptionsNewGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('subscriptions:new'))
        self.form = self.resp.context['form']

    def test_get(self):
        """GET /inscricao/ must return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use template subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """Html must contain input tags"""
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1))

        for tag, count in tags:
            with self.subTest():
                self.assertContains(self.resp, tag, count)

    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        #form = self.resp.context['form']
        self.assertIsInstance(self.form, SubscriptionForm)


class SubscriptionsNewPostValid(TestCase):
    """Tests for valid posts"""
    def setUp(self):
        self.data = dict(name="Bruno Santana", cpf="12345678901",
                         email="santanasta@gmail.com", phone="92-99410-4333")
        self.resp = self.client.post(r('subscriptions:new'), self.data)
        self.email = mail.outbox[0]

    def test_post(self):
        """Valid POST should redirect to /inscricao/1/"""
        self.assertRedirects(self.resp, r('subscriptions:detail', 1))

    def test_send_subscribe_email(self):
        """System must send email to user after subscription"""
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        """Post valid must be saved on model"""
        self.assertTrue(Subscription.objects.exists())


class SubscriptionsNewPostInvalid(TestCase):
    """tests for invalid posts"""
    def setUp(self):
        self.resp = self.client.post(r('subscriptions:new'), {})
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

    def test_dont_save_subscription(self):
        """Invalid post must not be saved on model"""
        self.assertFalse(Subscription.objects.exists())
