import logging

from botocore.exceptions import ClientError
from django.conf import settings
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

logger = logging.getLogger(settings.LOGGER_NAME)


def custom_exception_handler(exc: Exception, context: dict):
    response = None

    if isinstance(exc, Http404):
        response = Response(
            data={"message": "Nothing found here."}, status=status.HTTP_404_NOT_FOUND
        )

    elif isinstance(exc, DjangoPermissionDenied):
        response = Response(
            data={"message": "You are not allowed to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )

    elif isinstance(exc, APIException):
        headers = {}
        auth_header = getattr(exc, "auth_header", None)
        wait_header = getattr(exc, "wait", None)

        if auth_header:
            headers["WWW-Authenticate"] = auth_header
        if wait_header:
            headers["Retry-After"] = f"{wait_header}"

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {"message": exc.detail}

        response = Response(data, status=exc.status_code, headers=headers)

    elif isinstance(exc, AssertionError):
        if isinstance(exc.args[0], Response):
            response = exc.args[0]

    if response is None:
        response = Response(
            {"message": "Unknown error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

        if isinstance(exc, ClientError):
            error_data = {
                "message": "AWS ClientError",
                "response": exc.response,
                "operation_name": exc.operation_name,
            }
        else:
            error_data = {"message": "Unknown exception", "context": context}

        logger.exception(error_data, exc_info=exc)

    return response
