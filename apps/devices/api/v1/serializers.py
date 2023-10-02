from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.devices.models import Device


class DeviceSerializer(serializers.Serializer):
    id = serializers.CharField(
        max_length=20,
        required=True,
        allow_null=False,
        allow_blank=False,
        trim_whitespace=True,
        help_text=_("Device ID: `/devices/id123`"),
    )
    deviceModel = serializers.CharField(
        max_length=25,
        required=True,
        allow_null=False,
        allow_blank=False,
        trim_whitespace=True,
        help_text=_("Device Model ID: `/devicemodels/id123`"),
    )
    name = serializers.CharField(
        max_length=100,
        required=True,
        allow_null=False,
        allow_blank=False,
        trim_whitespace=True,
        help_text=_("Device Name"),
    )
    note = serializers.CharField(
        max_length=300,
        required=False,
        allow_null=True,
        allow_blank=True,
        trim_whitespace=True,
        help_text=_("Device Note"),
    )
    serial = serializers.CharField(
        max_length=10,
        required=True,
        allow_null=False,
        allow_blank=False,
        trim_whitespace=True,
        help_text=_("Device Serial"),
    )

    def validate_serial(self, value: str) -> str:
        if not value[0].isalpha() or not value[1:].isdigit():
            raise serializers.ValidationError(
                _("Serial number must be in the format of A000000001.")
            )

        return value

    def validate_id(self, value: str) -> int:
        try:
            assert value.startswith("/devices/id")
            return int(value.replace("/devices/id", ""))
        except (ValueError, AssertionError):
            raise serializers.ValidationError(_("Device ID is not valid."))

    def validate_deviceModel(self, value: str) -> int:
        try:
            assert value.startswith("/devicemodels/id")
            return int(value.replace("/devicemodels/id", ""))
        except (ValueError, AssertionError):
            raise serializers.ValidationError(_("Device Model ID is not valid."))

    def save(self, **kwargs) -> str:
        Device.add_or_update(
            device_id=self.validated_data["id"],
            device_model_id=self.validated_data["deviceModel"],
            name=self.validated_data["name"],
            note=self.validated_data.get("note") or "",
            serial=self.validated_data["serial"],
        )

        return f"/devices/id{self.validated_data['id']}"

    def to_representation(self, instance):
        return {
            "id": f"/devices/id{instance['id']}",
            "deviceModel": f"/devicemodels/id{instance['deviceModel']}",
            "name": instance["name"],
            "note": instance.get("note") or "",
            "serial": instance["serial"],
        }
