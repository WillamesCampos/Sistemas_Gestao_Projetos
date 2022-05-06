from datetime import datetime
import factory

from apps.turmas.models import Turma


class TurmaFactory(factory.django.DjangoModelFactory):

    nome = factory.Faker('company', locale='pt_BR')
    periodo = factory.Sequence(
        lambda n: datetime.now().strftime('%Y') + '.' + str((n % 3 + 1))
    )

    class Meta:
        model = Turma
