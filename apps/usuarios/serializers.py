from django.db import transaction
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import User ,Professor


class ProfessorSerializer(ModelSerializer):

    senha = serializers.CharField(
        max_length=50
    )
    confirmacao_senha = serializers.CharField(
        max_length=50,
        required = False
    )
    nova_senha = serializers.CharField(
        max_length=50,
        required = False
    )
    nome = serializers.CharField(
        max_length=250
    )
    email = serializers.EmailField()

    class Meta:
        model = Professor
        fields = [
            'codigo','nome', 'email', 'senha',
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

                if not check_password(dados.get('senha'), self.instance.password):
                    raise serializers.ValidationError(
                        'Senha incorreta.'
                    )

                valido = bool(
                    dados.get('confirmacao_senha', False) and dados.get('nova_senha', False)
                )

                if not valido:
                    raise serializers.ValidationError(
                        'Ao alterar a senha, a nova senha e a confirmação devem ser informados.'
                    )
                else:
                    if not dados.get('nova_senha') == dados.get('confirmacao_senha'):
                        raise serializers.ValidationError(
                            'A nova_senha e a confirmação da senha não conferem.'
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

class RecuperaSenhaSerializer(serializers.Serializer):
    email = serializers.EmailField()
    nova_senha = serializers.CharField()

    def validate(self, data):
        try:
            usuario = User.objects.get(email=data['email'])
        except:
            raise serializers.ValidationError(
                'E-mail de usuário não encontrado.'
                'Foi enviada uma chave de acesso ao e-mail cadastrado.'
            )

        return data


