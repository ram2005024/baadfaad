from django.contrib.auth import get_user_model, authenticate
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.models import Profile

USER_MODEL=get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    image=serializers.ImageField(allow_null=True,write_only=True,required=False)
    password2=serializers.CharField(max_length=50,write_only=True)
    password1=serializers.CharField(max_length=50,write_only=True)
    first_name=serializers.CharField(max_length=50)
    class Meta:
        model=USER_MODEL
        fields=["email","password1","password2","first_name","last_name","image"]

    def validate(self, attrs):
        password_1=attrs["password1"]
        password_2=attrs["password2"]
        if password_1!=password_2:
            raise serializers.ValidationError("Passwords don't match")
        attrs["first_name"]=(attrs.get("first_name") or "").title()
        attrs["last_name"]=(attrs.get("last_name") or "").title()
        return attrs
    @transaction.atomic
    def create(self, validated_data):
        image=validated_data.pop("image",None)
        password=validated_data.pop("password1")
        validated_data.pop("password2")
        user=USER_MODEL.objects.create_user(email=validated_data.pop("email"),password=password,**validated_data)
        Profile.objects.create(user=user,fullname=f"{user.first_name} {user.last_name}".strip(),image=image)
        return user


class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField(required=True)
    password=serializers.CharField(required=True,max_length=50)

    def validate(self,attrs):
        email=attrs["email"]
        password=attrs["password"]

        user=authenticate(request=self.context["request"],username=email,password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        refresh=RefreshToken.for_user(user)
        return {
            "access":str(refresh.access_token),
            "refresh":str(refresh)
        }