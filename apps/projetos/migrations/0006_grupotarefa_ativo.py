# Generated by Django 4.0.4 on 2022-05-15 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetos', '0005_tarefa_ativo'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupotarefa',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
    ]