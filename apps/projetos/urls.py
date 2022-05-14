from django.urls import path, include
from rest_framework import routers
from .views import ProjetoViewSet, GrupoViewSet, TarefaViewSet

router = routers.SimpleRouter()

router.register(
    'projetos',
    viewset=ProjetoViewSet,
    basename='projetos'
)

router.register(
    'grupos',
    viewset=GrupoViewSet,
    basename='grupos'
)

router.register(
    'tarefas',
    viewset=TarefaViewSet,
    basename='tarefas'
)

urlpatterns = [
    path('', include(router.urls))
]
