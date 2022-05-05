from random import choice
import factory
from apps.usuarios.models import Aluno


def gerar_matricula():
    matricula = ''

    for num in range(0, 12):
        matricula += str(
            choice(
                range(0, 10)
            )
        )

    return int(matricula)


class AlunoFactory(factory.django.DjangoModelFactory):

    nome = factory.Faker('name', locale='pt_BR')
    email = factory.Faker('email', locale='pt_BR')
    matricula = factory.Sequence(lambda n: str(gerar_matricula() + n))

    class Meta:
        model = Aluno
