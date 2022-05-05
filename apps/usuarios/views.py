
from django.contrib.auth.hashers import make_password
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework import status

from .models import User, Professor, Aluno
from .serializers import RecuperaSenhaSerializer
from .serializers import ProfessorSerializer, AlunoSerializer


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


class ProfessorViewSet(ModelViewSet):

    serializer_class = ProfessorSerializer
    queryset = Professor.objects.all()

    class Meta:
        model = Professor


class AlunoViewSet(ModelViewSet):
    serializer_class = AlunoSerializer
    queryset = Aluno.objects.all()

    class Meta:
        model: Aluno
