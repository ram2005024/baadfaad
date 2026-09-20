from rest_framework.response import Response


def success_response(
    message: str = "Success", data=None, status_code: int = 200
) -> Response:
    return Response(
        {
            "success": True,
            "message": message,
            "data": data,
        },
        status=status_code,
    )


def error_response(
    error_code: str = "UNKNOWN_ERROR",
    message: str = "Something went wrong",
    status_code: int = 500,
    details=None,
) -> Response:
    return Response(
        {
            "success": False,
            "message": message,
            "error_code": error_code,
            "details": details,
        },
        status=status_code,
    )
