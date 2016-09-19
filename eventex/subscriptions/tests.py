from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):
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
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        '''HTML must contains csrf'''
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        '''Context must have a subscription form'''
        self.assertIsInstance(self.form, SubscriptionForm)

    def test_form_has_fields(self):
        '''Form must have 4 fields'''
        self.assertSequenceEqual(
            ['name', 'cpf', 'email', 'phone'], list(self.form.fields))


class SubscribePostTest(TestCase):
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
        self.assertIn('Patrick Alves', self.email.body)
        self.assertIn('12345678901', self.email.body)
        self.assertIn('patrick@alves.net', self.email.body)
        self.assertIn('91-99999-0000', self.email.body)

class SubscribeInvalidPost(TestCase):
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




