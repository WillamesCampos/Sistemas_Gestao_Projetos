from django.db import transaction
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apps.core.validators import ValidaMatricula

from .models import User, Professor, Aluno


class ProfessorSerializer(ModelSerializer):

    senha = serializers.CharField(
        max_length=50
    )
    confirmacao_senha = serializers.CharField(
        max_length=50,
        required=False
    )
    nova_senha = serializers.CharField(
        max_length=50,
        required=False
    )

    class Meta:
        model = Professor
        fields = [
            'codigo', 'nome', 'email', 'senha',
            'nova_senha', 'confirmacao_senha'
        ]

    def to_representation(self, instance):
        return {
            'codigo': instance.codigo,
            'nome': instance.nome,
            'email': instance.email
        }

    def validate_email(self, email):
        if not self.instance:
            usuario = User.objects.filter(
                email=email
            )

            if usuario:
                raise serializers.ValidationError(
                    'Já existe um usuário cadastrado com o e-mail informado.'
                )

        return email

    def validate(self, dados):
        if self.instance:

            if dados.get('senha'):

                if not check_password(
                    dados.get('senha'), self.instance.password
                ):
                    raise serializers.ValidationError(
                        'Senha incorreta.'
                    )

                valido = bool(
                    dados.get('confirmacao_senha', False) and dados.get(
                        'nova_senha', False
                    )
                )

                if not valido:
                    raise serializers.ValidationError(
                        'Ao alterar a senha, a nova senha e a confirmação devem ser informados.' # noqa
                    )
                else:
                    if not dados.get('nova_senha') == dados.get(
                        'confirmacao_senha'
                    ):
                        raise serializers.ValidationError(
                            'A nova_senha e a confirmação da senha não conferem.' # noqa
                        )

        return dados

    def create(self, validated_data):

        with transaction.atomic():

            professor = Professor.objects.create(
                nome=validated_data['nome'],
                email=validated_data['email'],
                password=make_password(validated_data['senha'])
            )

        return professor

    def update(self, instance, validated_data):

        try:
            instance.password = make_password(
                validated_data.pop('nova_senha')
            )

            validated_data.pop('confirmacao_senha')
            validated_data.pop('senha')
        except KeyError:
            pass

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class AlunoSerializer(ModelSerializer):
    senha = serializers.CharField(
        max_length=50
    )
    confirmacao_senha = serializers.CharField(
        max_length=50,
        required=False
    )
    nova_senha = serializers.CharField(
        max_length=50,
        required=False
    )

    matricula = serializers.CharField(
        max_length=12,
        validators=[ValidaMatricula]
    )

    class Meta:
        model = Aluno
        fields = [
            'codigo', 'nome', 'email', 'matricula',
            'senha', 'nova_senha', 'confirmacao_senha'
        ]

    def to_representation(self, instance):
        return {
            'codigo': instance.codigo,
            'nome': instance.nome,
            'email': instance.email,
            'matricula': instance.matricula
        }

    def validate_email(self, email):
        try:
            Aluno.objects.get(email=email)
        except Aluno.DoesNotExist:
            return email

    def validate_matricula(self, matricula):
        try:
            aluno = Aluno.objects.get(matricula=matricula)
        except Aluno.DoesNotExist:
            return matricula

        if self.instance and aluno:
            return None

    def validate(self, dados):
        if self.instance:

            if dados.get('senha'):

                if not check_password(
                    dados.get('senha'), self.instance.password
                ):
                    raise serializers.ValidationError(
                        'Senha incorreta.'
                    )

                valido = bool(
                    dados.get('confirmacao_senha', False) and dados.get(
                        'nova_senha', False
                    )
                )

                if not valido:
                    raise serializers.ValidationError(
                        'Ao alterar a senha, a nova senha e a confirmação devem ser informados.' # noqa
                    )
                else:
                    if not dados.get('nova_senha') == dados.get(
                        'confirmacao_senha'
                    ):
                        raise serializers.ValidationError(
                            'A nova_senha e a confirmação da senha não conferem.' # noqa
                        )

        return dados

    def create(self, validated_data):

        return Aluno.objects.create(
            nome=validated_data['nome'],
            email=validated_data['email'],
            matricula=validated_data['matricula'],
            password=make_password(validated_data['senha'])
        )

    def update(self, instance, validated_data):
        try:
            instance.password = validated_data.pop('nova_senha')

            validated_data.pop('senha')
            validated_data.pop('confirmacao_senha')
        except KeyError:
            pass

        try:
            if validated_data['matricula'] is None:
                raise serializers.ValidationError(
                    'A matrícula informada não pode ser utilizada.'
                )
        except KeyError:
            pass

        return super().update(instance, validated_data)


class RecuperaSenhaSerializer(serializers.Serializer):
    email = serializers.EmailField()
    nova_senha = serializers.CharField()

    def validate(self, data):
        try:
            User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'E-mail de usuário não encontrado.'
                'Foi enviada uma chave de acesso ao e-mail cadastrado.'
            )

        return data
