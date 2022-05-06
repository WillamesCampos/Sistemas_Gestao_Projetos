from django.urls import path, include
from rest_framework import routers

from .views import TurmaViewSet


router = routers.SimpleRouter()

router.register(
    'turmas',
    viewset=TurmaViewSet,
    basename='turmas'
)

urlpatterns = [
    path('', include(router.urls))
]
