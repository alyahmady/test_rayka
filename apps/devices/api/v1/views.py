import random
import string

from botocore.exceptions import ClientError
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.devices.api.v1.serializers import DeviceSerializer
from apps.devices.models import Device


class DeviceCreateAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    throttle_scope = "device_create"

    def post(self, request, *args, **kwargs):
        serializer = DeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        device_id: str = serializer.save()

        return Response(data={"id": device_id}, status=status.HTTP_201_CREATED)


class DeviceRetrieveAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    throttle_scope = "device_retrieve"

    def get(self, request, *args, **kwargs):
        device = Device.get(kwargs["device_id"])
        if not device:
            return Response(
                data={"message": "Device not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = DeviceSerializer(instance=device, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
