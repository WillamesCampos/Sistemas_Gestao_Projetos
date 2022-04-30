from django.urls import path
from .views import RecuperaSenhaViewSet
from rest_framework.authtoken.views import ObtainAuthToken


urlpatterns = [
    path('login/', ObtainAuthToken.as_view(), name='obter_token_login'),
    path('recuperar-acesso/senha/', RecuperaSenhaViewSet.as_view({'patch': 'update'}), name='recuperar_acesso_login')
]
