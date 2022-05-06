from uuid import uuid4
from django.db import models


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

    class Meta:
        db_table = 'tb_turma'

    def __str__(self) -> str:
        return f'{self.codigo}'
