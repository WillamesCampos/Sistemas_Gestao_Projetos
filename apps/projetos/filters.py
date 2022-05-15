from django_filters import rest_framework as filters
from .models import Projeto, Grupo, Tarefa


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


class TarefaFilter(filters.FilterSet):
    disciplina = filters.CharFilter(
        field_name='projeto__disciplina__nome',
        lookup_expr='icontains'
    )
    projeto = filters.CharFilter(
        field_name='projeto__nome',
        lookup_expr='icontains'
    )
    professor = filters.CharFilter(
        field_name='projeto__professor__nome',
        lookup_expr='icontains'
    )
    nome = filters.CharFilter(
        lookup_expr='icontains'
    )
    situacao = filters.CharFilter(
        field_name='situacao',
        lookup_expr='icontains'
    )
    de_data = filters.DateFilter(
        field_name='data__date',
        lookup_expr='lte'
    )
    ate_data = filters.DateFilter(
        field_name='data__date',
        lookup_expr='gte'
    )
    descricao = filters.CharFilter(
        lookup_expr='icontains'
    )
    ativo = filters.BooleanFilter()

    class Meta:
        model = Tarefa
        fields = [
            'codigo'
        ]
