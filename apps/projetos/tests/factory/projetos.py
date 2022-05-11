import factory
from apps.projetos.models import Projeto, Grupo, ProjetoGrupo
from apps.turmas.tests.factory.turmas import DisciplinaFactory
from apps.usuarios.tests.factory.usuarios import (
    ProfessorFactory, AlunoFactory
)


class ProjetoFactory(factory.django.DjangoModelFactory):

    nome = factory.Faker('company', locale='pt_BR')
    descricao = 'Um projeto voltado para testes.'
    tipo = 'Teste'
    area = 'Testes Unitários'
    professor = factory.SubFactory(ProfessorFactory)

    class Meta:
        model = Projeto
        django_get_or_create = ['professor']


class GrupoFactory(factory.django.DjangoModelFactory):

    lider = factory.SubFactory(AlunoFactory)
    aluno = factory.SubFactory(AlunoFactory)
    disciplina = factory.SubFactory(DisciplinaFactory)
    ativo = True

    class Meta:
        model = Grupo
        django_get_or_create = ['aluno', 'lider', 'disciplina']


class ProjetoGrupoFactory(factory.django.DjangoModelFactory):

    projeto = factory.SubFactory(ProjetoFactory)
    grupo = factory.SubFactory(GrupoFactory)

    class Meta:
        model = ProjetoGrupo
