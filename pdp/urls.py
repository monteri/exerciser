from django.urls import include, path

from pdp.api.views import api

urlpatterns = [
    path("api/", include(api.urls)),
]
