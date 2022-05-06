from rest_framework import serializers

from apps.turmas.models import Turma
from apps.usuarios.models import Aluno


class TurmaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Turma
        fields = ['codigo', 'nome', 'periodo']


class AlunosTurmaSerializer(serializers.ModelSerializer):

    alunos = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(
            pk_field=serializers.UUIDField(
                format='hex_verbose'
            ),
            queryset=Aluno.objects.all()
        )
    )

    class Meta:
        model = Turma
        fields = ['alunos']

    def to_representation(self, instance):

        alunos = Aluno.objects.filter(
            turma=instance
        ).select_related('turma')

        return {
            'codigo': instance.codigo,
            'nome': instance.nome,
            'periodo': instance.periodo,
            'alunos': [
                {
                    "codigo": aluno.codigo,
                    "matricula": aluno.matricula,
                    "nome": aluno.nome
                } for aluno in alunos
            ]
        }

    def validate(self, data):
        if not data.get('alunos'):
            raise serializers.ValidationError(
                {
                    'alunos': 'Este campo é obrigatório. Deve ser informado pelo menos 1 aluno.' # noqa
                }
            )

        return data

    def update(self, instance, validated_data):
        try:
            if self.context['request'].remover_alunos:
                for aluno in validated_data['alunos']:
                    aluno.turma = None
        except AttributeError:
            for aluno in validated_data['alunos']:
                aluno.turma = instance

        Aluno.objects.bulk_update(
            validated_data['alunos'], ['turma']
        )

        return instance
