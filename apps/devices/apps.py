from django.apps import AppConfig

from apps.devices.models import Device


class DevicesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.devices"

    def ready(self):
        Device.create_table()
