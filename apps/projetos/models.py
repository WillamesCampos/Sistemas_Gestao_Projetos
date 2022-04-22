from uuid import uuid4
from django.db import models

from apps.usuarios.models import Aluno


class Grupo(models.Model):
    codigo = models.UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False
    )
    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.DO_NOTHING,
    )
    lider = models.OneToOneField(
        Aluno,
        on_delete=models.DO_NOTHING,
        related_name='lideres',
        related_query_name='lider'
    )


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
    grupo = models.OneToOneField(
        Grupo,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'tb_projeto'

    def __str__(self) -> str:
        return self.nome


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
    prazo = models.DateTimeField()
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


