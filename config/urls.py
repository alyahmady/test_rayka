from django.conf import settings
from django.urls import path, include


v1_apis = [
    path(
        f"{settings.API_PREFIX}/v1/devices/",
        include("apps.devices.api.v1.urls", namespace="devices-api"),
    )
]

urlpatterns = []

if settings.API_VERSION == "v1":
    urlpatterns.extend(v1_apis)
