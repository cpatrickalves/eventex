from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeGet(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')
        self.form = self.resp.context['form']

    def test_get(self):
        ''' Get /inscricao/ must return status code 200'''
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        ''' Must use subscriptions/subscription_form.html'''
        self.assertTemplateUsed(
            self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        '''Html must contain input tags'''
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1))

        for text, count in tags:
           with self.subTest():
               self.assertContains(self.resp, text, count)

    def test_csrf(self):
        '''HTML must contains csrf'''
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        '''Context must have a subscription form'''
        self.assertIsInstance(self.form, SubscriptionForm)


class SubscribePostValid(TestCase):
    def setUp(self):
        ''' Valid POST should redirect to /inscricao/'''
        data = dict(name='Patrick Alves', cpf='12345678901',
                    email='patrick@alves.net', phone='91-99999-0000')

        self.resp = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_post(self):
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))


class SubscribeInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})
        self.form = self.resp.context['form']

    def test_post(self):
        '''Invalid POST should not redirect'''
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        self.assertIsInstance(self.form, SubscriptionForm)

    def test_form_has_errors(self):
        self.assertTrue(self.form.errors)


class SubscribeSuccessMessage(TestCase):
    def setUp(self):
        data = dict(name='Patrick Alves', cpf='12345678901',
                    email='patrick@alves.net', phone='91-99999-0000')

        self.resp = self.client.post('/inscricao/', data, follow=True)

    def test_message(self):
        self.assertContains(self.resp, 'Inscrição realizada com sucesso!')



