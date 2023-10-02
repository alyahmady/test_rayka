from django.urls import path

from apps.devices.api.v1.views import (
    DeviceCreateAPIView,
    DeviceRetrieveAPIView,
)

app_name = "devices-api"


urlpatterns = [
    path("", DeviceCreateAPIView.as_view(), name="device-create"),
    path("<int:device_id>/", DeviceRetrieveAPIView.as_view(), name="device-retrieve"),
]
