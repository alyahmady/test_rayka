from django.urls import path

from apps.devices.api.v1.views import (
    DeviceCreateAPIView,
    DeviceRetrieveAPIView,
    CreateSampleDeviceModelsAPIView,
)

app_name = "devices-api"


urlpatterns = [
    path("", DeviceCreateAPIView.as_view(), name="device-create"),
    path(
        "create-fake-models/",
        CreateSampleDeviceModelsAPIView.as_view(),
        name="create-fake-device-models",
    ),  # Temporary
    path("<uuid:device_id>/", DeviceRetrieveAPIView.as_view(), name="device-retrieve"),
]
