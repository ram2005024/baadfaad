
from drf_spectacular.utils import  extend_schema, extend_schema_view, inline_serializer
from rest_framework import generics, serializers
from rest_framework.parsers import FormParser,MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user.exceptions import InvalidToken
from apps.user.serializer import RegisterSerializer, LoginSerializer
from config.env import env
from core.exceptions.base import AppException


class RegisterView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request=RegisterSerializer,
        tags=["Auth"],
        responses=inline_serializer("RegisterResponseSerializer",fields={
            "message":serializers.CharField()
        })
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return {
            "message":"User created successfully"
        }

@extend_schema_view(
    post=extend_schema(tags=["Auth"],responses=inline_serializer(
        "LoginResponse",
        fields={
            "access":serializers.CharField()
        }
    ))
)
class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response=Response(data={
                "access":serializer.validated_data["access"]
            },status=200)
        response.set_cookie(key="refresh",
                            value=serializer.validated_data["refresh"],
                            path="/",
                            httponly=True,
                            secure=env("SECURE"),
                            samesite=env("SAME_SITE"))
        return response

@extend_schema(request=None,tags=["Auth"],
responses=inline_serializer("RefreshViewSerializer",                                                      fields={
    "access":serializers.CharField()
}))
class RefreshView(TokenRefreshView):
        def post(self, request: Request, *args, **kwargs) -> Response:
            token=request.COOKIES.get("refresh",None)
            if not token:
                raise InvalidToken
            serializer=self.get_serializer(data={"refresh":token})
            try:
                serializer.is_valid(raise_exception=True)
            except:
                raise InvalidToken
            response=Response({
                "access":serializer.validated_data.get("access")
            })
            response.set_cookie(
                key="refresh",
                value=str(serializer.validated_data["refresh"]),
                httponly=True,
                samesite=env("SAME_SITE"),
                secure=env("SECURE")

            )
            return response

@extend_schema(tags=["Auth"])
class MeView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user