from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        f"{settings.API_PREFIX}/devices/",
        include("apps.devices.api.v1.urls", namespace="devices-api"),
    ),
]
