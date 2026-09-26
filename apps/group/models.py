from django.contrib.auth import get_user_model
from django.db import models

from common.base_model import BaseModel

User=get_user_model()



class Group(BaseModel):
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=100,null=True,blank=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name="created_groups")



class GroupMembership(BaseModel):
    group=models.ForeignKey(Group,related_name="memberships",on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="my_groups")

    class Meta:
        unique_together=("group","user")

class GroupInvitations(BaseModel):

    created_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name="created_invitations")
    token=models.CharField(max_length=100,unique=True)
    max_user_allowed=models.PositiveIntegerField(default=5)
    used_count=models.PositiveIntegerField(default=0)
    is_active=models.BooleanField(default=True)
    group=models.ForeignKey(Group,on_delete=models.CASCADE,related_name="invitations")

