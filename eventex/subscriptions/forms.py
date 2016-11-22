from django import forms
from django.core.exceptions import ValidationError


def validate_cpf(value):
    if not value.isdigit():
        raise ValidationError('CPF deve conter apenas números' , 'digits')
        # O 2o parâmetro é chamada de error code (utilizado nos testes)

    if len(value) != 11:
        raise ValidationError('CPF deve ter 11 números', 'length')


class SubscriptionForm(forms.Form):
    name = forms.CharField(label="Nome")
    cpf = forms.CharField(label="CPF", validators=[validate_cpf])
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Telefone")

    # Este é um método especial do django criado para cada field do formulário
    # Ele trata a entrada do formulário após a validação
    # Essa função sempre deve retornar algum valor
    def clean_name(self):
        name = self.cleaned_data['name']
        words = [w.capitalize() for w in name.split()]
        return ' '.join(words)

        

