from django.core.exceptions import ValidationError


def validate_cpf(value):
    if not value.isdigit():
        raise ValidationError('CPF deve conter apenas números' , 'digits')
        # O 2o parâmetro é chamada de error code (utilizado nos testes)

    if len(value) != 11:
        raise ValidationError('CPF deve ter 11 números', 'length')