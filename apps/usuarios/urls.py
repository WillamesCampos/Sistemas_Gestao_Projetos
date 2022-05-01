from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import ObtainAuthToken
from .views import RecuperaSenhaViewSet
from .views import ProfessorViewSet


router = routers.SimpleRouter()

router.register(
    'professores',
    viewset=ProfessorViewSet,
    basename='professores'
)


urlpatterns = [
    path('', include(router.urls))
]

urlpatterns = [
    path('login/', ObtainAuthToken.as_view(), name='obter_token_login'),
    path('recuperar-acesso/senha/', RecuperaSenhaViewSet.as_view({'patch': 'update'}), name='recuperar_acesso_login'),
    path('', include(router.urls))
]
