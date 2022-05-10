
from rest_framework import serializers
from .models import Projeto, Grupo, ProjetoGrupo
from apps.usuarios.models import Aluno, Professor
from apps.turmas.models import TurmaAluno


class ProjetoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projeto
        fields = [
            'codigo', 'nome', 'tipo', 'area', 'ativo'
        ]

    def to_representation(self, instance):

        try:
            grupos = [
                {
                    'codigo': grupo.codigo,
                    'quantidade_membros': len(grupo.participantes)
                } for grupo in instance._prefetched_objects_cache.get(
                    'grupo', None
                )
            ]
        except (TypeError, AttributeError):
            grupos = None

        return {
            'codigo': instance.codigo,
            'nome': instance.nome,
            'tipo': instance.tipo,
            'area': instance.area,
            'disponivel': instance.disponivel,
            'consolidado': instance.consolidado,
            'ativo': instance.ativo,
            'professor': {
                'codigo': instance.professor.codigo,
                'nome': instance.professor.nome
            },
            'grupos': grupos
        }

    def create(self, validated_data):

        projeto = Projeto.objects.create(
            nome=validated_data['nome'],
            tipo=validated_data['tipo'],
            area=validated_data['area'],
            professor=self.context['request'].professor
        )

        return projeto

    def update(self, instance, validated_data):
        if validated_data.get('ativo', None) is False:
            ProjetoGrupo.objects.filter(
                projeto=instance
            ).delete()

        instance.consolidado = False

        return super().update(instance, validated_data)


class ProjetoGrupoSerializer(serializers.ModelSerializer):

    MAX_GRUPOS = 12

    MIN_GRUPOS = 1

    grupo = serializers.PrimaryKeyRelatedField(
        pk_field=serializers.UUIDField(
            format='hex_verbose',
        ),
        queryset=Grupo.objects.all(),
        required=False
    )

    grupos_removidos = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(
            pk_field=serializers.UUIDField(
                format='hex_verbose',
            ),
            queryset=Grupo.objects.all(),
        ),
        required=False
    )

    class Meta:
        model = Projeto
        fields = ['grupo', 'consolidado', 'disponivel', 'grupos_removidos']

    def to_representation(self, instance):
        try:
            grupos = [
                {
                    'codigo': grupo.codigo,
                    'quantidade_membros': len(grupo.participantes)
                } for grupo in instance._prefetched_objects_cache.get(
                    'grupo', None
                )
            ]
        except TypeError:
            grupos = None

        return {
            'projeto': {
                'codigo': instance.codigo,
                'nome': instance.nome,
                'tipo': instance.tipo,
                'area': instance.area,
                'consolidado': instance.consolidado,
                'ativo': instance.ativo,
                'disponivel': instance.disponivel,
            },
            'grupos': grupos
        }

    def validate_grupo(self, grupo):

        if self.instance and grupo is not None:

            try:
                ProjetoGrupo.objects.get(
                    projeto=self.instance,
                    grupo=grupo
                )

                raise serializers.ValidationError(
                    'O grupo já está no projeto.'
                )
            except ProjetoGrupo.DoesNotExist:
                vagas_selecao = ProjetoGrupo.objects.filter(
                    projeto=self.instance
                ).count()

                if vagas_selecao == self.MAX_GRUPOS:
                    raise serializers.ValidationError(
                        'Não é possível adicionar mais grupos ao projeto'
                    )

                return grupo

    def validate(self, data):
        if not self.instance.ativo and not data.get('ativo', False):
            raise serializers.ValidationError(
                {
                    'ativo': [
                        'Um projeto deve estar ativo para ser gerenciado.'
                    ]
                }
            )

        if data.get('consolidado'):
            """
                Só consolida um projeto quando tem apenas 1 grupo associado.
            """
            grupos_no_projeto = ProjetoGrupo.objects.filter(
                projeto=self.instance
            ).count()

            if grupos_no_projeto < self.MIN_GRUPOS:
                raise serializers.ValidationError(
                    {
                        'consolidado': 'Não é possível consolidar projetos sem um grupo associado.' # noqa
                    }
                )
            elif not (grupos_no_projeto == self.MIN_GRUPOS):
                raise serializers.ValidationError(
                    {
                        'consolidado': 'Não é possível consolidar projetos com mais de um grupo associado.' # noqa
                    }
                )

        return data

    def update(self, instance, validated_data):
        if not instance.consolidado:
            """
                Associa o grupo a um projeto e consolida o projeto.
            """
            if validated_data.get('grupo', False):
                ProjetoGrupo.objects.create(
                    projeto=instance,
                    grupo=validated_data['grupo']
                )
                instance.consolidado = True
                validated_data.pop('grupo')
            elif validated_data.get('grupos_removidos'):
                ProjetoGrupo.objects.filter(
                    projeto=instance,
                    grupo__in=validated_data.get('grupos_removidos')
                ).delete()
                validated_data.pop('grupos_removidos')

        else:
            if validated_data.get('grupo', False):
                """
                    Não permite trocar um grupo quando o projeto
                    já está consolidado.
                """
                raise serializers.ValidationError(
                    {
                        'grupo': ['Torne o projeto não consolidado para vincular grupos.'] # noqa
                    }
                )

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return Projeto.objects.prefetch_related(
            'grupo'
        ).select_related(
            'professor'
        ).get(
            codigo=instance.codigo
        )


class GrupoSerializer(serializers.ModelSerializer):

    projetos = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(
            pk_field=serializers.UUIDField(
                format='hex_verbose'
            ),
            queryset=Projeto.objects.all()
        ),
        required=False
    )

    aluno = serializers.PrimaryKeyRelatedField(
        pk_field=serializers.UUIDField(
            format='hex_verbose'
        ),
        queryset=Aluno.objects.all(),
        required=False
    )

    class Meta:
        model = Grupo
        fields = ['aluno', 'projetos']

    def to_representation(self, instance):

        lider = {
            'codigo': instance.lider.codigo,
            'matricula': instance.lider.matricula,
            'lider': True
        }

        participantes = []
        participantes.append(lider)
        membros_grupo = [
            {
                'codigo': aluno.codigo,
                'matricula': aluno.matricula
            } for aluno in instance.participantes
        ]

        if membros_grupo:
            participantes += membros_grupo

        return {
            'codigo': instance.codigo,
            'ativo': instance.ativo,
            'disponivel': instance.disponivel,
            'participantes': participantes
        }

    def validate_aluno(self, aluno):

        turma = TurmaAluno.objects.filter(
            aluno=aluno
        )

        if not turma:
            raise serializers.ValidationError(
                'O aluno deve estar em uma turma.'
            )

        return aluno

    def validate_projetos(self, projetos):
        pass

    def create(self, validated_data):
        
        return Grupo.objects.create(
            lider=self.context['request'].aluno
        )
