
from core.exceptions.base import AppException
from rest_framework import status

class InvalidRequest(AppException):
    def __init__(
        self,
        message: str = "Invalid request.Please try again",
        error_code: str = "INVALID_REQUEST",
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        details=None,
    ):
        super().__init__(message, error_code, status_code, details)

