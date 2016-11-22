from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):
    def test_form_has_fields(self):
        '''Form must have 4 fields'''
        form = SubscriptionForm()
        expected = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_cpf_is_digit(self):
        ''' CPF must only accpet digit'''
        form = self.make_validator_form(cpf='ABCD5678901')  # usa o kwargs para a função
        self.assertFormErrorCode(form, 'cpf', 'digits') # Passa a chave e o code do erro

    def test_cpf_has_11_digits(self):
        ''' CPF must have 11 digits'''
        form = self.make_validator_form(cpf='1234') #usa o kwargs para a função
        self.assertFormErrorCode(form, 'cpf', 'length')  # Passa a chave e o code do erro

    def test_name_must_be_capitalized(self):
        """Name must be capitalized"""
        form = self.make_validator_form(name='PATRICK alves')
        # O cleaned_data é um dicionário que armazena todos os valores do
        # formulários já validados
        self.assertEqual('Patrick Alves', form.cleaned_data['name'])


    # Compara o código do erro
    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)

    # Compara a mensagem de erro
    def assertFormErrorMessage(self, form, field, msg):
        errors = form.errors
        errors_list = errors[field]
        self.assertListEqual([msg], errors_list)

    def make_validator_form(self, **kwargs):
        valid = dict(name='Patrick Alves', cpf='12345678901',
                    email='patrick@alves.net', phone='91-00009999')

        data = dict(valid, **kwargs)
        form = SubscriptionForm(data)  # Instancia o formulário
        form.is_valid()  # Chama as rotinas de validação
        return form