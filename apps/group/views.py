from rest_framework.response import Response

from apps.group.schema import GroupPaginationSerializer
from core.responses.api_response import get_paginated_serializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.group.models import Group
from apps.group.serilaizer import GroupSerializer
from core.pagination.base import StandardPagination





@extend_schema_view(
    list=extend_schema(
        tags=["Group Endpoints"],
        responses=GroupPaginationSerializer
    )
)
class GroupViewSet(ModelViewSet):
    pagination_class = StandardPagination
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    queryset = Group.objects.prefetch_related("memberships__user__profile")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
