from datetime import datetime

from django.test import TestCase
from eventex.subscriptions.models import Subscription

class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name='Patrick Alves',
            cpf='987987987-98',
            email='patrick@alves.com',
            phone='91-000009898'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        ''' Subscription must have an auto created_at attr'''
        self.assertIsInstance(self.obj.created_at, datetime)

