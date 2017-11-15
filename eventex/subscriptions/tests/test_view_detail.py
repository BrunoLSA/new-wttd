from django.test import TestCase
from eventex.subscriptions.models import Subscription
from django.shortcuts import resolve_url as r


class SubscriptionDetailGet(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name='Bruno Santana',
            cpf='12345678901',
            email='santanasta@gmail.com',
            phone='92-99410-4333'
        )
        self.obj.save()

        self.resp = self.client.get(r('subscriptions:detail', self.obj.pk))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_detail.html')

    def test_context(self):
        self.assertIsInstance(self.obj, Subscription)

    def test_html(self):
        contents = (self.obj.name, self.obj.cpf,
                    self.obj.email, self.obj.phone)
        with self.subTest():
            for expected in contents:
                self.assertContains(self.resp, expected)


class SubscriptionDetailNotFound(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('subscriptions:detail', 0))

    def test_not_found(self):
        self.assertEqual(404, self.resp.status_code)