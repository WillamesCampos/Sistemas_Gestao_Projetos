# Generated by Django 4.0.4 on 2022-05-14 19:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('projetos', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='tarefa',
            table='tb_tarefa',
        ),
        migrations.CreateModel(
            name='GrupoTarefa',
            fields=[
                ('codigo', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('data_criacao', models.DateTimeField(auto_now=True)),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projetos.grupo')),
                ('tarefa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projetos.tarefa')),
            ],
            options={
                'db_table': 'tb_grupo_tarefa',
            },
        ),
    ]
