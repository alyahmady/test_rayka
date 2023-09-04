import uuid

from botocore.exceptions import ClientError
from django.utils.translation import gettext_lazy as _
from mypy_boto3_dynamodb.service_resource import Table
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.devices.models import DeviceModel, Device


class DeviceSerializer(serializers.Serializer):
    id = serializers.UUIDField(
        required=False, default=uuid.uuid1, help_text=_("Device ID")
    )
    deviceModel = serializers.UUIDField(
        required=True, help_text=_("Device Model ID")
    )
    name = serializers.CharField(
        max_length=100, required=True, help_text=_("Device Name")
    )
    note = serializers.CharField(
        max_length=255,
        required=False,
        allow_null=True,
        help_text=_("Device Note"),
    )
    serial = serializers.CharField(
        max_length=10, required=True, help_text=_("Device Serial")
    )

    def validate(self, attrs: dict) -> dict:
        attrs["serial"] = attrs["serial"].strip()
        if not attrs["serial"][0].isalpha() or not attrs["serial"][1:].isdigit():
            raise serializers.ValidationError(
                {"serial": _("Serial number must be in the format of A000000001.")}
            )

        if "id" not in attrs:
            attrs["id"] = uuid.uuid1()

        device_model_table: Table = DeviceModel()
        device_model_id: dict = (
            device_model_table.get_item(
                Key={DeviceModel.id: attrs["deviceModel"].hex},
                ProjectionExpression=DeviceModel.id,
                ConsistentRead=False,
                ReturnConsumedCapacity="NONE",
            )
            .get("Item", {})
            .get(DeviceModel.id, None)
        )
        if device_model_id != attrs["deviceModel"].hex:
            raise ValidationError({"deviceModel": _("Device Model ID does not exist.")})

        return attrs

    def save(self, **kwargs) -> uuid.UUID:
        device_table: Table = Device()

        try:
            # TODO logging and monitoring with `ConsumedCapacity` object in response
            device_table.put_item(
                Item={
                    Device.id: self.validated_data["id"].hex,
                    Device.model_id: self.validated_data["deviceModel"].hex,
                    Device.name: self.validated_data["name"],
                    Device.note: self.validated_data.get("note"),
                    Device.serial: self.validated_data["serial"],
                },
                ConditionExpression=f"attribute_not_exists({Device.id})",
                ReturnValues="NONE",
                ReturnConsumedCapacity="NONE",
                ReturnItemCollectionMetrics="NONE",
            )

        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ConditionalCheckFailedException":
                raise ValidationError({"id": _("Device ID already exists.")}) from exc
            raise exc

        return self.validated_data["id"]
