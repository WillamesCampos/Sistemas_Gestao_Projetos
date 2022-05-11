from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.core.permissions import (
    ConcretePermissionAluno, ConcretePermissionProfessor
)
from apps.turmas.models import Turma, Disciplina
from apps.turmas.serializers import (
    DisciplinaSerializer, TurmaSerializer, AlunosTurmaSerializer
)


class DisciplinaViewSet(ModelViewSet):

    serializer_class = DisciplinaSerializer
    permission_classes = [
        IsAuthenticated, ConcretePermissionProfessor
    ]

    def get_queryset(self):
        return Disciplina.objects.filter(
            professor=self.request.professor,
            ativo=True
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.ativo = False
        instance.save()

        return Response(
            status=status.HTTP_204_NO_CONTENT
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
            - Aluno: Só pode ver a turma que está cadastrado uma vez que for
            cadastrado. Se ainda não estiver cadastrado, vê as turmas do
            professor.
            - Professor: Pode ver todas as turmas dele.
        """
        if hasattr(self.request, 'aluno'):
            try:
                turmas = Turma.objects.prefetch_related(
                    'aluno'
                ).filter(
                    aluno=self.request.aluno
                ).select_related('professor')

                if turmas:
                    return turmas
                else:
                    return Turma.objects.all().select_related(
                        'professor'
                    ).prefetch_related(
                        'aluno'
                    )
            except AttributeError:
                pass

        return Turma.objects.filter(
            professor=self.request.professor
        ).select_related(
            'professor'
        ).prefetch_related(
            'aluno'
        )

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return super().get_permissions()
        elif self.action in ['participar']:
            return [ConcretePermissionAluno()]
        else:
            return [ConcretePermissionProfessor()]

    @action(
        methods=['patch'],
        detail=True,
        url_path='participar',
        url_name='participar',
        serializer_class=AlunosTurmaSerializer,
        permission_classes=[
            IsAuthenticated
        ]
    )
    def participar(self, request, pk):
        """
            Inserir alunos em uma turma.
            - Os alunos podem se inserir em uma turma
            gerenciada por um professor.
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
            IsAuthenticated
        ]
    )
    def remover_alunos(self, request, pk):
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
