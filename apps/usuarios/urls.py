from django.urls import include, path
from rest_framework import routers

from .views import LoginViewSet

router = routers.SimpleRouter()


urlpatterns = [
    path('login/', LoginViewSet.as_view())
]
