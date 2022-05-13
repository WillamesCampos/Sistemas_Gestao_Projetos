from uuid import uuid4
from django.db import models

from apps.usuarios.models import Professor, Aluno


class Disciplina(models.Model):
    codigo = models.UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False
    )
    nome = models.CharField(
        max_length=100
    )
    nota_corte = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=5.0
    )
    quantidade_grupos = models.IntegerField(
        default=1
    )
    professor = models.ForeignKey(
        Professor,
        on_delete=models.DO_NOTHING
    )
    ativo = models.BooleanField(
        default=True
    )

    class Meta:
        db_table = 'tb_disciplina'

    def __str__(self) -> str:
        return self.codigo


class Turma(models.Model):
    codigo = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )
    nome = models.CharField(
        max_length=30
    )
    periodo = models.CharField(
        max_length=6
    )
    aluno = models.ManyToManyField(
        Aluno,
        through='TurmaAluno',
        blank=True
    )
    professor = models.ForeignKey(
        Professor,
        on_delete=models.DO_NOTHING,
        related_name='professor'
    )
    disciplina = models.ForeignKey(
        Disciplina,
        on_delete=models.DO_NOTHING
    )
    ativo = models.BooleanField(
        default=True
    )

    class Meta:
        db_table = 'tb_turma'

    def __str__(self) -> str:
        return f'{self.codigo}'


class TurmaAluno(models.Model):
    codigo = models.UUIDField(
        default=uuid4,
        editable=False,
        primary_key=True
    )
    turma = models.ForeignKey(
        Turma,
        on_delete=models.DO_NOTHING
    )
    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.DO_NOTHING
    )

    class Meta:
        db_table = 'tb_turmaaluno'

    def __str__(self) -> str:
        return f'{self.codigo}'
