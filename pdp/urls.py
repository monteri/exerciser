from django.urls import path, include
from .views import api

urlpatterns = [
    path("api/", include(api.urls)),
]