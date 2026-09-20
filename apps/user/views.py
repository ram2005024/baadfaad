from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView


class UserListView(APIView):
    @extend_schema(tags=["Users"])
    def get(self, request):
        return Response({"users": []})


class UserDetailView(APIView):
    @extend_schema(tags=["Users"])
    def get(self, request, pk):
        return Response({"user_id": pk})
