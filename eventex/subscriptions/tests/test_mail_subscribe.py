from django.test import TestCase
from django.core import mail
from django.shortcuts import resolve_url as r


class SubscribePostValid(TestCase):
    """Tests for valid posts"""
    def setUp(self):
        self.data = dict(name="Bruno Santana", cpf="12345678901",
                         email="santanasta@gmail.com", phone="92-99410-4333")
        self.client.post(r('subscriptions:new'), self.data)
        self.email = mail.outbox[0]

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
        contents = [
            'Bruno Santana',
            '12345678901',
            'santanasta@gmail.com',
            '92-99410-4333'
        ]

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)


