from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.core.permissions import (
    ConcretePermissionAluno, ConcretePermissionProfessor
)
from apps.turmas.models import Turma
from apps.turmas.serializers import (
    TurmaSerializer, AlunosTurmaSerializer
)


class TurmaViewSet(ModelViewSet):

    serializer_class = TurmaSerializer
    permission_classes = [
        ConcretePermissionProfessor
        | ConcretePermissionAluno
    ]

    class Meta:
        model = Turma

    def get_queryset(self):
        """
            Retorna as turmas de acordo com o usuário.
            - Aluno: Só pode ver a turma que está cadastrado.
            - Professor: Pode ver todas as turmas.
        """
        try:
            if self.request.aluno:
                return Turma.objects.filter(
                    aluno=self.request.aluno
                )
        except AttributeError:
            return Turma.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return super().get_permissions()
        else:
            return [ConcretePermissionProfessor()]

    @action(
        methods=['patch'],
        detail=True,
        url_path='adicionar-alunos',
        url_name='adicionar-alunos',
        serializer_class=AlunosTurmaSerializer,
        permission_classes=[
            IsAuthenticated,
            ConcretePermissionProfessor
        ]
    )
    def inserir_alunos_turma(self, request, pk):
        """
            Inserir alunos em uma turma.
            - Apenas professores inserem
            alunos de uma turma.
            - Se um aluno já estiver em uma turma,
            será sobrescrita pela informada na
            requisição.
        """
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response(
            serializer.data
        )

    @action(
        methods=['patch'],
        detail=True,
        url_path='remover-alunos',
        url_name='remover-alunos',
        serializer_class=AlunosTurmaSerializer,
        permission_classes=[
            IsAuthenticated,
            ConcretePermissionProfessor
        ]
    )
    def remover_alunos_turma(self, request, pk):
        """
            Remove todos os alunos em uma turma.
            - Apenas professores removem
            alunos de uma turma.
        """

        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        request.remover_alunos = True

        self.perform_update(serializer)

        return Response(
            serializer.data
        )
