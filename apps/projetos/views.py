from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from .models import (
    Projeto, ProjetoGrupo, Grupo
)
from .serializers import (
    ProjetoGrupoSerializer, ProjetoSerializer,
    GrupoSerializer
)

from rest_framework.permissions import IsAuthenticated
from apps.core.permissions import (
    ConcretePermissionProfessor,
    ConcretePermissionAluno
)


class ProjetoViewSet(ModelViewSet):

    serializer_class = ProjetoSerializer
    permission_classes = [
        IsAuthenticated, ConcretePermissionProfessor
    ]

    class Meta:
        model = Projeto

    def get_queryset(self):
        return Projeto.objects.prefetch_related(
            'grupo'
        ).select_related('professor').filter(
            professor=self.request.professor
        )

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        ProjetoGrupo.objects.filter(
            projeto=instance
        ).delete()

        instance.delete()

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

    def get_queryset(self):
        return Grupo.objects.filter(
            Q(aluno=self.request.aluno)
            | Q(lider=self.request.aluno)
        )

    class Meta:
        model = Grupo
