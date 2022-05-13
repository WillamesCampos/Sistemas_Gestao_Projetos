from django.contrib.auth.hashers import make_password
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework import status

from .models import User, Professor, Aluno
from .serializers import RecuperaSenhaSerializer
from .serializers import ProfessorSerializer, AlunoSerializer

from .tasks import celery_email_cadastro


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
    queryset = Aluno.objects.prefetch_related(
        'aluno'
    ).all()

    class Meta:
        model: Aluno


class CadastroViewSet(GenericViewSet, CreateModelMixin):

    authentication_classes = ()
    permission_classes = ()

    def get_serializer_class(self):
        if self.request.query_params.get('usuario') == 'aluno':
            return AlunoSerializer
        else:
            return ProfessorSerializer

    def create(self, request, *args, **kwargs):
        if request.query_params.get('usuario') == 'aluno':
            serializer = self.get_serializer(data=request.data)
        elif request.query_params.get('usuario') == 'professor':
            serializer = self.get_serializer(data=request.data)
        else:
            return Response(
                data='Não foi possível efetuar o cadastro.',
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        celery_email_cadastro.delay(
            'Seja Bem-Vindo!',
            'Você acabou de se cadastrar no Sistema de Gestão de Projetos.',
            request.data['email']
        )

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
