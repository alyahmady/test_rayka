import logging

from botocore.exceptions import ClientError
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(settings.LOGGER_NAME)


def custom_exception_handler(exc: Exception, context: dict):
    response = exception_handler(exc, context)

    if response is None:
        response = Response(
            {"message": "Unknown error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

        if isinstance(exc, ClientError):
            logger.exception(
                {
                    "message": "AWS ClientError",
                    "response": exc.response,
                    "operation_name": exc.operation_name,
                },
                exc_info=exc,
            )
        else:
            logger.exception(
                {"message": "Unknown exception", "context": context}, exc_info=exc
            )

    return response
