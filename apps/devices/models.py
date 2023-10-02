from typing import Literal

from botocore.exceptions import ClientError

from config.dynamodb import BaseTable


class Device(BaseTable):
    _table_name: str = "rayka_test_devices_aahmadi"

    id: str = "id"
    model_id: str = "deviceModel"
    name: str = "name"
    note: str = "note"
    serial: str = "serial"

    def __new__(cls):
        cls._init_table()
        return cls._table

    @classmethod
    def add_or_update(
        cls,
        device_id: int,
        device_model_id: int,
        name: str,
        note: str | None,
        serial: str,
    ) -> dict:
        cls._init_table()

        # TODO logging on ConsumedCapacity and ItemCollectionMetrics
        return cls._table.put_item(
            Item={
                cls.id: device_id,
                cls.model_id: device_model_id,
                cls.name: name,
                cls.note: note or "",
                cls.serial: serial,
            },
            ReturnValues="NONE",
            ReturnConsumedCapacity="NONE",
            ReturnItemCollectionMetrics="NONE",
        )

    @classmethod
    def get(cls, device_id: int):
        cls._init_table()

        # TODO monitoring ThrottlingException on ConsistentReads
        return cls._table.get_item(
            Key={cls.id: device_id},
            ProjectionExpression=f"{cls.id},#deviceName,{cls.model_id},{cls.note},{cls.serial}",
            ExpressionAttributeNames={"#deviceName": cls.name},
            ConsistentRead=False,
        ).get("Item", None)

    @classmethod
    def delete(cls, device_id: int):
        cls._init_table()

        try:
            response = cls._table.delete_item(
                Key={cls.id: device_id},
                ConditionExpression=f"attribute_exists({cls.id})",
                ReturnValues="NONE",
                ReturnConsumedCapacity="NONE",
                ReturnItemCollectionMetrics="NONE",
            )
        except ClientError as exc:
            if exc.response["Error"]["Code"] != "ConditionalCheckFailedException":
                raise exc

            response = None

        return response
