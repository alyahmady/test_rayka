from django.apps import AppConfig

from apps.devices.models import Device, DeviceModel


class DevicesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.devices"

    def ready(self):
        Device.create_table()
        DeviceModel.create_table()
