from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.user.serializer import RegisterSerializer
from core.responses.api_response import success_response


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(message="User created successfully")
