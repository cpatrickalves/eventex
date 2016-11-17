from unittest.mock import Mock

from django.test import TestCase
from eventex.subscriptions.admin import SubscriptionModelAdmin, Subscription, admin


class SubscriptionModelAdminTest(TestCase):
    def setUp(self):
        # Prepara o BD
        Subscription.objects.create(name='Patrick alves', cpf='12345678901',
                                    email='patrick@alves.net', phone='91-00003333')

        self.model_admin = SubscriptionModelAdmin(Subscription, admin.site)


    def test_has_action(self):
        ''' Action mark_as_paid should be installed '''
        self.assertIn('mark_as_paid', self.model_admin.actions)


    def test_mark_all(self):
        ''' It should mark all selected subscriptions as paid '''

        self.call_action()
        self.assertEqual(1, Subscription.objects.filter(paid=True).count())


    def test_message(self):
        '''It shoulf send a message to the user'''
                # Monta uma Query

        mock = self.call_action()
        mock.assert_called_once_with(None, '1 inscrição foi marcada como paga.')


    def call_action(self):
        # Monta uma Query
        queryset = Subscription.objects.all()

        mock = Mock()
        old_message_user = SubscriptionModelAdmin.message_user
        SubscriptionModelAdmin.message_user = mock

        # Chama a Action
        self.model_admin.mark_as_paid(None, queryset)
        SubscriptionModelAdmin.message_user = old_message_user

        return mock