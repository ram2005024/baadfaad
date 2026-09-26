from rest_framework import status

from core.exceptions.base import AppException


class InvalidUser(AppException):
    def __init__(
        self,
        message: str = "Invalid User",
        error_code: str = "INVALID_USER",
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details=None,
    ):
        super().__init__(message, error_code, status_code, details)


class InvalidToken(AppException):
    def __init__(
        self,
        message: str = "Invalid Token",
        error_code: str = "INVALID_TOKEN",
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        details=None,
    ):
        super().__init__(message, error_code, status_code, details)


class VerificationError(AppException):
    def __init__(
        self,
        message: str = "Please verify your account",
        error_code: str = "VERIFICATION_ERROR",
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        details=None,
    ):
        super().__init__(message, error_code, status_code, details)


class TokenExpired(AppException):
    def __init__(
        self,
        message: str = "Token expired",
        error_code: str = "TOKEN_EXPIRED",
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        details=None,
    ):
        super().__init__(message, error_code, status_code, details)


class MaximumAttempt(AppException):
    def __init__(
        self,
        message: str = "Maximum attempt",
        error_code: str = "MAXIMUM_ATTEMPT",
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        details=None,
    ):
        super().__init__(message, error_code, status_code, details)


class InvalidCode(AppException):
    def __init__(
        self,
        message="Invalid Code",
        error_code="INVALID_CODE",
        status_code=status.HTTP_401_UNAUTHORIZED,
        details=None,
    ):
        super().__init__(message, error_code, status_code, details)


class UserAlreadyVerified(AppException):
    def __init__(
        self,
        message="User already verified",
        error_code="USER_ALREADY_VERIFIED",
        status_code=status.HTTP_400_BAD_REQUEST,
        details=None,
    ):
        super().__init__(message, error_code, status_code, details)

class InvalidOrExpiredToken(AppException):
    def __init__(self,message="Invalid or Expired Token",error_code="INVALID_OR_EXPIRED_TOKEN",status_code=status.HTTP_400_BAD_REQUEST):
        super().__init__(message,error_code,status_code,details=None)
