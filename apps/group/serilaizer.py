from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.group.models import GroupMembership

User=get_user_model()

class GroupMemberSerializer(serializers.ModelSerializer):
    full_name=serializers.CharField(source="profile.full_name",read_only=True),
    image=serializers.ImageField(source="profile.image",read_only=True,allow_null=True,allow_empty_file=True)
    class Meta:
        model=User
        fields=[
            "id",
            "email",
            "full_name",
            "image"
        ]



class GroupMembershipSerializer(serializers.ModelSerializer):
    user=GroupMemberSerializer(read_only=True)
    class Meta:
        model=GroupMembership
        fields=["user"]




class GroupSerializer(serializers.ModelSerializer):
    memberships=GroupMembershipSerializer(many=True)
    user_ids=serializers.ListField(default=[],child=serializers.UUIDField(),required=False,write_only=True)
    class Meta:
        fields=[
            "id",
            "name",
            "description",
            "memberships"
            "user_ids"
        ]
        read_only_fields=[
            "id",
            "memberships"
        ]