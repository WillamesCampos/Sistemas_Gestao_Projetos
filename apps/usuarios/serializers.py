from rest_framework import serializers
from .models import User


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


