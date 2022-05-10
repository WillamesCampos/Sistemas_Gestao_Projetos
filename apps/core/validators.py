from rest_framework.serializers import ValidationError
from re import match

def ValidaMatricula(matricula):
    if len(matricula) != 12:
        message = 'A matrícula deve ter 12 caracteres.'
        raise ValidationError(message)

    if not str(matricula).isdecimal():
        message = 'Devem ser informados apenas números na matrícula.'
        raise ValidationError(message)

    return matricula


def ValidaPeriodo(periodo):
    if len(periodo) != 6:
        message = 'O período deve ter 6 caracteres.'
        raise ValidationError(message)

    if not match(r'\d{4}.\d{1}$', periodo):
        message = 'Formato do período deve ser dddd.d, ex: 1111.1'
        raise ValidationError(message)
