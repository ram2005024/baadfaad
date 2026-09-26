from typing import Any
from urllib.parse import uses_fragment

from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer
from rest_framework import generics, serializers, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView, set_rollback
from rest_framework_simplejwt.views import TokenRefreshView

from apps.user.exceptions import InvalidToken, VerificationError
from apps.user.models import User
from apps.user.serializer import (
    LoginSerializer,
    RegisterSerializer,
    ResendSerializer,
    UserSerializer,
    VerifySerializer, ForgetSerializer, ResetSerializer,
)
from apps.user.services import VerificationService
from apps.user.tasks import send_verification_message, send_reset_link_message
from config.env import env


class RegisterView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request=RegisterSerializer,
        tags=["Auth"],
        responses=inline_serializer(
            "RegisterResponseSerializer", fields={"message": serializers.CharField()}
        ),
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_verification_message.delay(str(user.id))
        return Response(
            {"message": "User created successfully.Please verify your account."},
            status=201,
        )


@extend_schema_view(
    post=extend_schema(
        tags=["Auth"],
        responses=inline_serializer(
            "LoginResponse", fields={"access": serializers.CharField()}
        ),
    )
)
class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if not user.is_verified:
            has_verification_sent = VerificationService().has_sent_verification_code(
                user.id
            )
            if not has_verification_sent:
                send_verification_message.delay(user.id)
            raise VerificationError
        response = Response(
            data={"access": serializer.validated_data["access"]}, status=200
        )
        response.set_cookie(
            key="refresh",
            value=serializer.validated_data["refresh"],
            path="/",
            httponly=True,
            secure=env("SECURE"),
            samesite=env("SAME_SITE"),
        )
        return response


@extend_schema(
    request=None,
    tags=["Auth"],
    responses=inline_serializer(
        "RefreshViewSerializer", fields={"access": serializers.CharField()}
    ),
)
class RefreshView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        token = request.COOKIES.get("refresh", None)
        if not token:
            raise InvalidToken
        serializer = self.get_serializer(data={"refresh": token})
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            raise InvalidToken
        response = Response({"access": serializer.validated_data.get("access")})
        response.set_cookie(
            key="refresh",
            value=str(serializer.validated_data["refresh"]),
            httponly=True,
            samesite=env("SAME_SITE"),
            secure=env("SECURE"),
        )
        return response


@extend_schema(tags=["Auth"])
class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return User.objects.select_related("profile").get(pk=self.request.user.pk)


@extend_schema(tags=["Auth"])
class VerifyView(APIView):
    serializer_class = VerifySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


@extend_schema(tags=["Auth"])
class ResendView(generics.CreateAPIView):
    serializer_class = ResendSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

@extend_schema(tags=["Auth"],responses=inline_serializer(name="ForgetResponseSerializer",fields={
    "message":serializers.CharField()
}))
class PasswordForgetView(generics.CreateAPIView):
    serializer_class = ForgetSerializer

    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token=serializer.validated_data["token"]
        user_id=serializer.validated_data["user_id"]
        if VerificationService.has_reset_sent(user_id):
            return Response({"message": "Reset url has been sent to your email"}, status=status.HTTP_200_OK)
        send_reset_link_message.delay(token,user_id)
        return Response({"message":"Reset url has been sent to your email"},status=status.HTTP_200_OK)
@extend_schema(tags=["Auth"],
               request=ResetSerializer,responses=inline_serializer(name="ResetSerializerResponse",fields={
    "message":serializers.CharField()
}))
class PasswordResetView(APIView):
    def post(self):
        serializer=ResetSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            "message":"Password reset successfully"
        })