from datetime import datetime
import factory

from apps.turmas.models import Disciplina, Turma, TurmaAluno
from apps.usuarios.tests.factory.usuarios import AlunoFactory, ProfessorFactory


class DisciplinaFactory(factory.django.DjangoModelFactory):

    nome = factory.Faker('company', locale='pt_BR')
    nota_corte = 5.0
    professor = factory.SubFactory(ProfessorFactory)

    class Meta:
        model = Disciplina
        django_get_or_create = ['professor']


class TurmaFactory(factory.django.DjangoModelFactory):

    nome = factory.Faker('company', locale='pt_BR')
    periodo = factory.Sequence(
        lambda n: datetime.now().strftime('%Y') + '.' + str((n % 3 + 1))
    )
    professor = factory.SubFactory(ProfessorFactory)
    disciplina = factory.SubFactory(DisciplinaFactory)

    class Meta:
        model = Turma
        django_get_or_create = ['professor', 'disciplina']


class TurmaAlunoFactory(factory.django.DjangoModelFactory):

    aluno = factory.SubFactory(AlunoFactory)
    turma = factory.SubFactory(TurmaFactory)

    class Meta:
        model = TurmaAluno
        django_get_or_create = ['turma']
