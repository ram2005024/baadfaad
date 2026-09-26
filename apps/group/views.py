from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from apps.group.models import Group
from apps.group.serilaizer import GroupSerializer
from core.pagination.base import StandardPagination


@extend_schema(tags=["Group Endpoints"])
class GroupViewSet(ModelViewSet):
    pagination_class = StandardPagination
    serializer_class = GroupSerializer
    queryset = Group.objects.prefetch_related("memberships__user__profile")
