from django import forms
from django.core.exceptions import ValidationError
from eventex.subscriptions.models import Subscription


class SubscriptionForm(forms.ModelForm):

    # define o modelo e os campos do modelo a serem utilizados
    class Meta:
        model = Subscription
        fields = ['name', 'cpf', 'email', 'phone']

    # Este é um método especial do django criado para cada field do formulário
    # Ele trata a entrada do formulário após a validação
    # Essa função sempre deve retornar algum valor
    def clean_name(self):
        name = self.cleaned_data['name']
        words = [w.capitalize() for w in name.split()]
        return ' '.join(words)

    # Esté e o clean do form todo
    # É chamado depois que todos os campos são validados
    # Util para se analisar 2 campos simultaneamente
    # Deve sempre retornar os dados válidos
    def clean(self):
        # Evita que esse clean sobreescreva o clean no ModelForm
        self.cleaned_data = super().clean()

        if not self.cleaned_data.get('email') and not self.cleaned_data.get('phone'):
            raise ValidationError('Informe seu e-mail ou telefone.')

        return self.cleaned_data