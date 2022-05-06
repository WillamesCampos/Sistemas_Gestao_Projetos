from abc import abstractmethod
from rest_framework.permissions import BasePermission

from apps.usuarios.models import DjangoCustomUser


class BaseUsuarioPermission(BasePermission):

    @abstractmethod
    def has_permission(self, request, view):
        pass


class AlunoPermission(BaseUsuarioPermission):

    def has_permission(self, request, view):
        try:
            aluno = request.user.aluno
            request.aluno = aluno
            return True
        except (
            DjangoCustomUser.aluno.RelatedObjectDoesNotExist,
            AttributeError
        ):
            return False


class ProfessorPermission(BaseUsuarioPermission):
    def has_permission(self, request, view):
        try:
            professor = request.user.professor
            request.professor = professor
            return True
        except (
            DjangoCustomUser.professor.RelatedObjectDoesNotExist,
            AttributeError
        ):
            return False


class ConcretePermissionAluno(BaseUsuarioPermission):

    def has_permission(self, request, view):
        return AlunoPermission().has_permission(request, view)


class ConcretePermissionProfessor(BaseUsuarioPermission):

    def has_permission(self, request, view):
        return ProfessorPermission().has_permission(request, view)
