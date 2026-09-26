from django.contrib.auth import get_user_model
from django.db import models

from common.base_model import BaseModel

User=get_user_model()



class Group(BaseModel):
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=100,null=True,blank=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name="owned_groups")



class GroupMembership(BaseModel):
    group=models.ForeignKey(Group,related_name="memberships",on_delete=models.DB_CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="groups")

    class Meta:
        unique_together=("group","user")


