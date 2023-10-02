import logging

import boto3
from botocore.exceptions import ClientError
from django.conf import settings

logger = logging.getLogger(settings.LOGGER_NAME)


class DynamoDBClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DynamoDBClient, cls).__new__(cls)
            cls._instance = boto3.client("dynamodb")
        return cls._instance


class DynamoDBResource:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DynamoDBResource, cls).__new__(cls)
            cls._instance = boto3.resource("dynamodb")
        return cls._instance


class BaseTable:
    _table = None
    _table_name: str = None

    @classmethod
    def _init_table(cls):
        table_name = (
            cls._table_name
            if (not settings.TESTING)
            else f"{cls._table_name}_testing"
        )

        if not cls._table or cls._table.name != table_name:
            resource = DynamoDBResource()
            cls._table = resource.Table(table_name)

    @classmethod
    def create_table(cls: "BaseTable") -> None:
        if not hasattr(cls, "id"):
            cls.id = "id"

        if not cls._table_name:
            raise NotImplementedError("`_table_name` must be defined in subclass")

        if not cls._table_name.startswith(settings.PROJECT_KEY):
            raise ValueError(f"`_table_name` must start with `{settings.PROJECT_KEY}_`")

        client = DynamoDBClient()

        table_name = (
            cls._table_name if (not settings.TESTING) else f"{cls._table_name}_testing"
        )

        try:
            client.create_table(
                TableName=table_name,
                AttributeDefinitions=[{"AttributeName": cls.id, "AttributeType": "N"}],
                KeySchema=[{"AttributeName": cls.id, "KeyType": "HASH"}],
                ProvisionedThroughput={
                    "ReadCapacityUnits": settings.DDB_TABLE_READ_CAPACITY_UNITS,
                    "WriteCapacityUnits": settings.DDB_TABLE_WRITE_CAPACITY_UNITS,
                },
            )
            client.get_waiter("table_exists").wait(
                TableName=table_name,
                WaiterConfig={"Delay": 5, "MaxAttempts": 10},
            )

        except ClientError as exc:
            if exc.response["Error"]["Code"] != "ResourceInUseException":
                logger.exception("Error creating table", exc_info=exc)
                raise exc

    @classmethod
    def delete_table(cls):
        if not settings.TESTING:
            raise NotImplementedError("This method is only for testing")

        if not cls._table_name:
            raise NotImplementedError("`_table_name` must be defined in subclass")

        if not cls._table_name.startswith(settings.PROJECT_KEY):
            raise ValueError(f"`_table_name` must start with `{settings.PROJECT_KEY}_`")

        client = DynamoDBClient()

        table_name = f"{cls._table_name}_testing"
        try:
            client.delete_table(TableName=table_name)
            client.get_waiter("table_not_exists").wait(
                TableName=table_name, WaiterConfig={"Delay": 5, "MaxAttempts": 10}
            )

        except ClientError as exc:
            if exc.response["Error"]["Code"] != "ResourceNotFoundException":
                logger.exception("Error deleting table", exc_info=exc)
                raise exc
