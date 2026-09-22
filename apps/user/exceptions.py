from rest_framework import status

from core.exceptions.base import AppException


class InvalidUser(AppException):
    def __init__(
        self,
        message: str = "Invalid User",
        error_code: str = "INVALID_USER",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details=None,
    ):
        super().__init__(message, error_code, status_code, details)
