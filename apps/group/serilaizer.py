from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.group.models import GroupMembership, Group

User=get_user_model()



class GroupMemberSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(source="user.id")
    email=serializers.EmailField(source="user.email")
    full_name=serializers.CharField(source="user.profile.full_name")
    image=serializers.CharField(source="user.profile.image")

    class Meta:
        model=GroupMembership
        fields=["id",
            "email",
            "full_name",
            "image"]




class GroupSerializer(serializers.ModelSerializer):
    memberships=GroupMemberSerializer(many=True,read_only=True)
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
        membership_ids=validated_data.pop("user_ids",[])
        request=self.context.get("request")
        creator=getattr(request,"user",None)
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

