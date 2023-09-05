import logging

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from mypy_boto3_dynamodb.service_resource import Table

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
    _table: Table = None
    _table_name: str = None

    @classmethod
    def create_table(cls: "BaseTable") -> None:
        if not hasattr(cls, "id"):
            cls.id = "id"

        if not cls._table_name:
            raise NotImplementedError("`_table_name` must be defined in subclass")

        # Must
        if not cls._table_name.startswith(settings.PROJECT_KEY):
            raise ValueError(F"`_table_name` must start with `{settings.PROJECT_KEY}_`")

        client = DynamoDBClient()
        # TODO Retry, MaxAttempts and CapacityUnits should be configurable (not magic)
        try:
            client.create_table(
                TableName=cls._table_name,
                AttributeDefinitions=[{"AttributeName": cls.id, "AttributeType": "S"}],
                KeySchema=[{"AttributeName": cls.id, "KeyType": "HASH"}],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5,
                },
            )
            client.get_waiter("table_exists").wait(
                TableName=cls._table_name,
                WaiterConfig={"Delay": 5, "MaxAttempts": 10},
            )

        except ClientError as exc:
            if exc.response["Error"]["Code"] != "ResourceInUseException":
                logger.exception("Error creating table", exc_info=exc)
                raise exc
