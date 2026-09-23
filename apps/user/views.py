from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.user.serializer import RegisterSerializer, LoginSerializer
from config.env import env
from core.responses.api_response import success_response


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message="User created successfully")

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response=success_response(
            data={
                "access":serializer.validated_data["access"]
            }
        )
        response.set_cookie(key="refresh",
                            value=serializer.validated_data["refresh"],
                            path="/api/v1/auth/login",
                            httponly=True,
                            secure=env("SECURE"),
                            samesite=env("SAME_SITE"))
        return response