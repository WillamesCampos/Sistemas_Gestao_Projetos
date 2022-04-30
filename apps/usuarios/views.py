from django.contrib.auth.hashers import make_password
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import RecuperaSenhaSerializer


class RecuperaSenhaViewSet(GenericViewSet, UpdateModelMixin):

    authentication_classes = ()
    permission_classes = ()

    serializer_class = RecuperaSenhaSerializer

    def update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        usuario = User.objects.get(email=serializer.data['email'])

        usuario.password = make_password(serializer.data['nova_senha'])

        usuario.save()

        return Response(
            status=status.HTTP_200_OK
        )