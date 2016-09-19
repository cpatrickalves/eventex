from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        ''' Valid POST should redirect to /inscricao/'''
        data = dict(name='Patrick Alves', cpf='12345678901',
                    email='patrick@alves.net', phone='91-99999-0000')

        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = "Confirmação de Inscrição"
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br', 'patrick@alves.net']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = ['Patrick Alves',
                    '12345678901',
                    'patrick@alves.net',
                    '91-99999-0000']

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
