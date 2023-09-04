import logging

from django.conf import settings
from mypy_boto3_dynamodb.service_resource import Table

from config.dynamodb import BaseTable, DynamoDBResource

logger = logging.getLogger(settings.LOGGER_NAME)


class DeviceModel(BaseTable):
    _table_name: str = "rayka_test_device_models"

    def __new__(cls) -> Table:
        if not cls._table:
            resource = DynamoDBResource()
            cls._table = resource.Table(cls._table_name)

        return cls._table

    id: str = "id"
    name: str = "name"


class Device(BaseTable):
    _table_name: str = "rayka_test_devices"

    def __new__(cls) -> Table:
        if not cls._table:
            resource = DynamoDBResource()
            cls._table = resource.Table(cls._table_name)

        return cls._table

    id: str = "id"
    model_id: str = "deviceModel"
    name: str = "name"
    note: str = "note"
    serial: str = "serial"
