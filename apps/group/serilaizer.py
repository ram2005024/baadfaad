from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.group.models import GroupMembership, Group

User=get_user_model()

class GroupMemberSerializer(serializers.ModelSerializer):
    full_name=serializers.CharField(source="profile.full_name",read_only=True)
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
        model=Group
        fields=[
            "id",
            "name",
            "description",
            "memberships",
            "user_ids"
        ]
        read_only_fields=[
            "id",
            "memberships"
        ]
    @transaction.atomic
    def create(self, validated_data):
        membership_ids=validated_data.pop("user_ids",None)
        creator=validated_data.get("created_by",None)
        group=Group.objects.create(**validated_data)
        if creator:
            membership_ids.append(creator.id)
        if membership_ids:
            users=User.objects.filter(id__in=membership_ids)
            GroupMembership.objects.bulk_create(
                    GroupMembership(user=user,group=group)
                 for user in users
            )
        return group

