from django.urls import path, include
from rest_framework import routers

from .views import DisciplinaViewSet, TurmaViewSet


router = routers.SimpleRouter()

router.register(
    'turmas',
    viewset=TurmaViewSet,
    basename='turmas'
)

router.register(
    'disciplinas',
    viewset=DisciplinaViewSet,
    basename='disciplinas'
)

urlpatterns = [
    path('', include(router.urls))
]
