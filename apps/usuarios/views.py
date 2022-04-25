from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import (AuthenticationFailed, NotAuthenticated)
from .models import Professor, Aluno


class LoginViewSet(APIView):

    def post(self, request, *args, **kwargs):
        usuario = super().authenticate(request)

        # return super().create(request, *args, **kwargs)
        if not usuario:
            raise AuthenticationFailed()

        super().enforce_csrf(request)
