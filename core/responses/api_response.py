from drf_spectacular.utils import inline_serializer
from rest_framework import serializers
from rest_framework.response import Response




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


def get_paginated_serializer(serializer, name=None):
    return inline_serializer(
        name=name or f"{serializer.__name__}List",
        fields={
            "pages": serializers.IntegerField(),
            "has_next": serializers.BooleanField(),
            "has_previous": serializers.BooleanField(),
            "total": serializers.IntegerField(),
            "filtered": serializers.IntegerField(),
            "data": serializer(many=True),
        },
    )