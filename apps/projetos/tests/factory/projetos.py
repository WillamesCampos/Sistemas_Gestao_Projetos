import factory
from apps.projetos.models import GrupoTarefa, Projeto, Grupo, ProjetoGrupo, Tarefa
from apps.turmas.tests.factory.turmas import DisciplinaFactory
from apps.usuarios.tests.factory.usuarios import (
    ProfessorFactory, AlunoFactory
)
from datetime import datetime, timedelta


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


class TarefaFactory(factory.django.DjangoModelFactory):
    nome = factory.Faker('company', locale='pt_BR')
    descricao = 'Uma tarefa para um projeto'
    data = datetime.now().strftime("%d/%m/%Y")
    hora = datetime.now().strftime("%H:%M:%S")
    situacao = 'pendente'
    responsavel = factory.SubFactory(AlunoFactory)
    projeto = factory.SubFactory(ProjetoFactory)
    ativo = True

    class Meta:
        model = Tarefa
        django_get_or_create = ['projeto', 'responsavel']


class GrupoTarefaFactory(factory.django.DjangoModelFactory):
    tarefa = factory.SubFactory(TarefaFactory)
    grupo = factory.SubFactory(GrupoFactory)

    class Meta:
        model = GrupoTarefa
        django_get_or_create = ['tarefa', 'grupo']