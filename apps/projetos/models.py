from uuid import uuid4
from django.db import models

from apps.usuarios.models import Aluno, Professor
from apps.turmas.models import Disciplina


class Grupo(models.Model):
    codigo = models.UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False
    )
    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.DO_NOTHING,
        null=True
    )
    lider = models.OneToOneField(
        Aluno,
        on_delete=models.DO_NOTHING,
        related_name='lideres',
        related_query_name='lider'
    )
    ativo = models.BooleanField(
        default=False
    )
    disponivel = models.BooleanField(
        default=True
    )
    disciplina = models.ForeignKey(
        Disciplina,
        on_delete=models.DO_NOTHING
    )

    @property
    def participantes(self):
        """Método que lista os participantes do grupo.

        Returns:
            [list]: [Código dos alunos que pertencem ao grupo]
        """
        membros = Aluno.objects.filter(
            grupo__codigo=self.codigo
        )

        return membros

    class Meta:
        db_table = 'tb_grupo'

    def __str__(self) -> str:
        return f'{self.codigo}'


class Projeto(models.Model):
    codigo = models.UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False
    )
    nome = models.CharField(
        max_length=50
    )
    descricao = models.TextField()
    tipo = models.CharField(
        max_length=20
    )
    area = models.CharField(
        max_length=20
    )
    grupo = models.ManyToManyField(
        Grupo,
        through='ProjetoGrupo',
        blank=True,
    )
    professor = models.ForeignKey(
        Professor,
        on_delete=models.DO_NOTHING
    )
    disponivel = models.BooleanField(
        default=True
    )
    ativo = models.BooleanField(
        default=True
    )
    consolidado = models.BooleanField(
        default=False
    )
    disciplina = models.ForeignKey(
        Disciplina,
        on_delete=models.DO_NOTHING
    )

    class Meta:
        db_table = 'tb_projeto'

    def __str__(self) -> str:
        return f'{self.codigo}'


class ProjetoGrupo(models.Model):
    codigo = models.UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False
    )
    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.DO_NOTHING
    )
    grupo = models.ForeignKey(
        Grupo,
        on_delete=models.DO_NOTHING
    )
    data_selecao_projeto = models.DateTimeField(
        auto_now=True
    )

    @property
    def data_selecao_formatada(self):
        return self.data_selecao_projeto.strftime(
            "%d/%m/%Y %H:%M:%S"
        )

    class Meta:
        db_table = 'tb_projeto_grupo'
        ordering = ['data_selecao_projeto']
        verbose_name_plural = 'Projetos Grupos'

    def __str__(self) -> str:
        return f'{self.codigo}'


class Tarefa(models.Model):
    codigo = models.UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False
    )
    nome = models.CharField(
        max_length=40
    )
    descricao = models.TextField()
    data = models.DateField()
    hora = models.DateTimeField()
    situacao = models.CharField(
        max_length=10
    )
    projeto = models.OneToOneField(
        Projeto,
        on_delete=models.DO_NOTHING
    )
    responsavel = models.OneToOneField(
        Aluno,
        on_delete=models.DO_NOTHING,
        null=True
    )
    ativo = models.BooleanField(
        default=True
    )

    @property
    def prazo_formatado(self):
        data = self.data.strftime(
            "%d/%m/%Y"
        )
        hora = self.hora.strftime(
            "%H:%M:%S"
        )

        return f'{data} {hora}'

    class Meta:
        db_table = 'tb_tarefa'

    def __str__(self) -> str:
        return self.codigo


class GrupoTarefa(models.Model):
    codigo = models.UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False
    )
    tarefa = models.ForeignKey(
        Tarefa,
        on_delete=models.CASCADE,
    )
    grupo = models.ForeignKey(
        Grupo,
        on_delete=models.CASCADE
    )
    data_criacao = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = 'tb_grupo_tarefa'

    def __str__(self) -> str:
        return self.codigo

