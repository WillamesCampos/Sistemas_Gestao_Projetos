from django_filters import rest_framework as filters
from .models import Projeto, Grupo


class GrupoFilter(filters.FilterSet):

    disciplina = filters.UUIDFilter(
        field_name='disciplina'
    )
    aluno = filters.UUIDFilter(
        field_name='aluno'
    )
    lider = filters.UUIDFilter(
        field_name='lider'
    )

    class Meta:
        model = Grupo
        fields = ['codigo', 'ativo', 'disponivel', 'aluno', 'lider']


class ProjetoFilter(filters.FilterSet):

    disciplina = filters.UUIDFilter(
        field_name='disciplina'
    )
    professor = filters.UUIDFilter(
        field_name='professor'
    )

    class Meta:
        model = Projeto
        fields = [
            'codigo', 'ativo', 'disponivel', 'nome', 'area',
            'tipo', 'ativo', 'consolidado'
        ]
