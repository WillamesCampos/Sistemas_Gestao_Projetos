from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import ObtainAuthToken
from .views import RecuperaSenhaViewSet
from .views import ProfessorViewSet, AlunoViewSet, CadastroViewSet


router = routers.SimpleRouter()

router.register(
    'professores',
    viewset=ProfessorViewSet,
    basename='professores'
)

router.register(
    'alunos',
    viewset=AlunoViewSet,
    basename='alunos'
)


urlpatterns = [
    path('cadastre-se/', CadastroViewSet.as_view({'post': 'create'}), name='cadastro'), # noqa
    path('login/', ObtainAuthToken.as_view(), name='obter_token_login'),
    path('recuperar-acesso/senha/', RecuperaSenhaViewSet.as_view({'patch': 'update'}), name='recuperar_acesso_login'), # noqa
    path('', include(router.urls))
]
