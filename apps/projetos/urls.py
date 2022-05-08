from django.urls import path, include
from rest_framework import routers
from .views import ProjetoViewSet

router = routers.SimpleRouter()

router.register(
    'projetos',
    viewset=ProjetoViewSet,
    basename='projetos'
)

urlpatterns = [
    path('', include(router.urls))
]
