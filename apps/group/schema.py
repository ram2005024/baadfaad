from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from apps.group.serilaizer import GroupSerializer


@extend_schema_serializer(many=False)
class GroupPaginationSerializer(serializers.Serializer):
    pages = serializers.IntegerField()
    has_next = serializers.BooleanField()
    has_previous = serializers.BooleanField()
    total = serializers.IntegerField()
    data = GroupSerializer(many=True)