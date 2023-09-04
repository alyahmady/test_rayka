import random
import string
import uuid

from botocore.exceptions import ClientError
from mypy_boto3_dynamodb.service_resource import Table
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.devices.api.v1.serializers import DeviceSerializer
from apps.devices.models import Device, DeviceModel


class DeviceCreateAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    throttle_scope = "device_create"

    def post(self, request, *args, **kwargs):
        serializer = DeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        device_id = serializer.save()

        return Response(data={"id": device_id}, status=status.HTTP_201_CREATED)


class DeviceRetrieveAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    throttle_scope = "device_retrieve"
    lookup_field = "id"
    lookup_url_kwarg = "device_id"

    def get(self, request, *args, **kwargs):
        device_table: Table = Device()

        # TODO monitoring ThrottlingException on ConsistentReads
        try:
            device = device_table.get_item(
                Key={Device.id: kwargs["device_id"].hex},
                ProjectionExpression=f"{Device.id},#deviceName,{Device.model_id},{Device.note},{Device.serial}",
                ExpressionAttributeNames={'#deviceName': Device.name},
                ConsistentRead=False,
            )["Item"]
        except LookupError:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DeviceSerializer(data=device, many=False)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


# Temporary
class CreateSampleDeviceModelsAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        device_model_table: Table = DeviceModel()

        device_model_ids = []

        for _ in range(10):
            try:
                device_model_id = uuid.uuid1()
                device_model_name = "".join(
                    random.choice(string.ascii_letters) for _ in range(10)
                )

                device_model_table.put_item(
                    Item={
                        DeviceModel.id: device_model_id.hex,
                        DeviceModel.name: device_model_name,
                    },
                    ConditionExpression=f"attribute_not_exists({DeviceModel.id})",
                    ReturnValues="NONE",
                    ReturnConsumedCapacity="NONE",
                    ReturnItemCollectionMetrics="NONE",
                )

            except ClientError:
                pass

            else:
                device_model_ids.append(str(device_model_id))

        return Response(data=device_model_ids, status=status.HTTP_201_CREATED)
