from rest_framework import serializers
from apps.core.validators import ValidaPeriodo

from apps.turmas.models import Turma, TurmaAluno, Disciplina
from apps.usuarios.models import Aluno


class DisciplinaSerializer(serializers.ModelSerializer):

    nota_corte = serializers.DecimalField(
        min_value=1,
        max_digits=5,
        decimal_places=2
    )
    quantidade_grupos = serializers.IntegerField(
        min_value=1
    )

    class Meta:
        model = Disciplina
        exclude = ['professor']

    def to_representation(self, instance):
        return {
            'codigo': instance.codigo,
            'nome': instance.nome,
            'nota_corte': float(instance.nota_corte),
            'quantidade_grupos': instance.quantidade_grupos,
            'professor': {
                'nome': instance.professor.nome
            }
        }

    def create(self, validated_data):
        return Disciplina.objects.create(
            professor=self.context['request'].professor,
            nome=validated_data['nome'],
            nota_corte=validated_data['nota_corte'],
            quantidade_grupos=validated_data['quantidade_grupos']
        )


class TurmaSerializer(serializers.ModelSerializer):

    alunos = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(
            pk_field=serializers.UUIDField(
                format='hex_verbose'
            ),
            queryset=Aluno.objects.all()
        ),
        required=False,
        min_length=1
    )
    disciplina = serializers.PrimaryKeyRelatedField(
        pk_field=serializers.UUIDField(
            format='hex_verbose'
        ),
        queryset=Disciplina.objects.all()
    )

    periodo = serializers.CharField(
        validators=[ValidaPeriodo]
    )

    class Meta:
        model = Turma
        fields = ['codigo', 'nome', 'periodo', 'alunos', 'disciplina']

    def to_representation(self, instance):
        return {
            'codigo': instance.codigo,
            'nome': instance.nome,
            'disciplina': {
                'codigo': instance.disciplina.codigo,
                'nome': instance.disciplina.nome
            },
            'periodo': instance.periodo,
            'professor': {
                'codigo': instance.professor.codigo,
                'nome': instance.professor.nome
            }
        }

    def create(self, validated_data):
        return Turma.objects.create(
            nome=validated_data['nome'],
            periodo=validated_data['periodo'],
            professor=self.context['request'].professor,
            disciplina=validated_data['disciplina']
        )

    def update(self, instance, validated_data):

        if validated_data.get('alunos'):
            turma_alunos = []
            for aluno in validated_data['alunos']:
                turma_alunos.append(
                    TurmaAluno(
                        turma=instance,
                        aluno=aluno
                    )
                )

            TurmaAluno.objects.bulk_create(turma_alunos)
            validated_data.pop('alunos')

        return super().update(instance, validated_data)


class AlunosTurmaSerializer(serializers.Serializer):

    alunos = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(
            pk_field=serializers.UUIDField(
                format='hex_verbose'
            ),
            queryset=Aluno.objects.all()
        ),
        required=False
    )

    def to_representation(self, instance):

        professor = {
            'codigo': instance.professor.codigo,
            'nome': instance.professor.nome,
            'email': instance.professor.email
        } if instance.professor else None

        try:
            alunos_obj = instance._prefetched_objects_cache[
                'aluno'
            ]

            alunos = [
                {
                    "codigo": aluno.codigo,
                    "matricula": aluno.matricula,
                    "nome": aluno.nome
                } for aluno in alunos_obj
            ]
        except (AttributeError, KeyError):
            alunos = None

        return {
            'codigo': instance.codigo,
            'nome': instance.nome,
            'periodo': instance.periodo,
            'professor': professor,
            'alunos': alunos
        }

    def update(self, instance, validated_data):

        if hasattr(
            self.context['request'],
            'remover_alunos'
        ) and validated_data.get('alunos'):
            TurmaAluno.objects.filter(
                turma=instance,
                aluno__in=validated_data['alunos']
            ).delete()
        else:
            aluno = Aluno.objects.get(
                codigo=self.context['request'].aluno.codigo
            )
            TurmaAluno.objects.create(
                turma=instance,
                aluno=aluno
            )

        return Turma.objects.select_related(
            'professor'
        ).prefetch_related(
            'aluno'
        ).get(
            codigo=instance.codigo
        )
