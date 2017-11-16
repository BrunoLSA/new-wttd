from datetime import datetime

from django.test import TestCase
from eventex.subscriptions.models import Subscription


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name='Bruno Santana',
            cpf='12345678901',
            email='santanasta@gmail.com',
            phone='92-99410-4333'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        """Subscription must have na auto created_at attr"""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        """Must return the name of the object"""
        self.assertEqual('Bruno Santana', str(self.obj))

    def test_paid_default_to_False(self):
        """By default, paid must be False"""
        self.assertEqual(False, self.obj.paid)