from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from .models import (
    Projeto, ProjetoGrupo, Grupo, Tarefa
)
from .serializers import (
    ProjetoGrupoSerializer, ProjetoSerializer,
    GrupoSerializer, TarefaSerializer
)
from .filters import GrupoFilter, ProjetoFilter, TarefaFilter

from rest_framework.permissions import IsAuthenticated
from apps.core.permissions import (
    ConcretePermissionProfessor,
    ConcretePermissionAluno
)


class ProjetoViewSet(ModelViewSet):

    serializer_class = ProjetoSerializer
    permission_classes = [
        IsAuthenticated, ConcretePermissionProfessor
        | ConcretePermissionAluno
    ]
    filterset_class = ProjetoFilter

    class Meta:
        model = Projeto

    def get_permissions(self):
        try:
            if self.request.user.aluno and self.action in ['list', 'retrieve']:
                return [ConcretePermissionAluno()]
        except (TypeError, AttributeError):
            return super().get_permissions()

    def get_queryset(self):
        if hasattr(self.request, 'professor'):
            return Projeto.objects.prefetch_related(
                'grupo'
            ).select_related('professor').filter(
                professor=self.request.professor,
                disciplina__professor=self.request.professor
            )
        else:
            return Projeto.objects.all()

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        ProjetoGrupo.objects.filter(
            projeto=instance
        ).delete()

        instance.ativo = False
        instance.save()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        methods=['patch'],
        detail=True,
        serializer_class=ProjetoGrupoSerializer,
        url_path='gerenciar-grupos',
        url_name='gerenciar-grupos',
    )
    def gerenciar_grupos(self, request, pk=None):

        instance = self.get_object()

        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response(
            serializer.data
        )


class GrupoViewSet(ModelViewSet):

    permission_classes = [
        IsAuthenticated,
        ConcretePermissionAluno
    ]
    serializer_class = GrupoSerializer
    filterset_class = GrupoFilter

    def get_permissions(self):
        try:
            if self.request.user.professor:
                if self.action in ['list', 'retrieve', 'ativar']:
                    return [ConcretePermissionProfessor()]
        except (TypeError, AttributeError):
            return super().get_permissions()

    def get_queryset(self):
        if hasattr(self.request, 'aluno'):
            grupos = Grupo.objects.filter(
                Q(aluno=self.request.aluno)
                | Q(lider=self.request.aluno),
                ativo=True
            )

            if grupos:
                return grupos
            else:
                return Grupo.objects.all()

        return Grupo.objects.all()

    class Meta:
        model = Grupo

    @action(
        methods=['patch'],
        detail=True,
        url_path='participar',
        url_name='participar'
    )
    def participar_grupos(self, request, pk):
        pass


class TarefaViewSet(ModelViewSet):

    permission_classes = [
        IsAuthenticated,
        ConcretePermissionProfessor
    ]
    serializer_class = TarefaSerializer
    filterset_class = TarefaFilter

    class Meta:
        model = Tarefa

    def get_permissions(self):
        try:
            if self.request.user.aluno:
                if self.action in ['list', 'retrieve']:
                    return [ConcretePermissionAluno()]
        except (TypeError, AttributeError):
            return super().get_permissions()

    def get_queryset(self):
        return Tarefa.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.ativo = False
        instance.save()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
