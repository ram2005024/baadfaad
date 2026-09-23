
from drf_spectacular.utils import extend_schema_serializer, extend_schema, extend_schema_view, inline_serializer
from rest_framework import generics, serializers
from rest_framework.parsers import FormParser,MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.user.serializer import RegisterSerializer, LoginSerializer
from config.env import env

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
                            path="/api/v1/auth/login",
                            httponly=True,
                            secure=env("SECURE"),
                            samesite=env("SAME_SITE"))
        return response