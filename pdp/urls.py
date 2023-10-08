from django.urls import path

from pdp.api.views import api

urlpatterns = [
    path("", api.urls),
]
