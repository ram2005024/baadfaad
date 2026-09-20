from rest_framework import status as http_status


class AppException(Exception):
    def __init__(
        self,
        message: str = "Something went wrong",
        error_code: str = "APP_ERROR",
        status_code: int = http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        details=None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)
