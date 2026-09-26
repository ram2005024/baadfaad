from typing import Any

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.exceptions import (
    InvalidCode,
    MaximumAttempt,
    TokenExpired,
    UserAlreadyVerified, InvalidToken, InvalidOrExpiredToken,
)
from apps.user.models import Profile
from apps.user.services import VerificationService
from apps.user.tasks import send_verification_message
from core.exceptions.common import InvalidRequest

USER_MODEL = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_null=True, write_only=True, required=False)
    password2 = serializers.CharField(max_length=50, write_only=True)
    password1 = serializers.CharField(max_length=50, write_only=True)
    first_name = serializers.CharField(max_length=50)

    class Meta:
        model = USER_MODEL
        fields = ["email", "password1", "password2", "first_name", "last_name", "image"]

    def validate(self, attrs):
        password_1 = attrs["password1"]
        password_2 = attrs["password2"]
        if password_1 != password_2:
            raise serializers.ValidationError("Passwords don't match")
        attrs["first_name"] = (attrs.get("first_name") or "").title()
        attrs["last_name"] = (attrs.get("last_name") or "").title()
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        image = validated_data.pop("image", None)
        password = validated_data.pop("password1")
        validated_data.pop("password2")
        user = USER_MODEL.objects.create_user(
            email=validated_data.pop("email"), password=password, **validated_data
        )
        Profile.objects.create(
            user=user,
            full_name=f"{user.first_name} {user.last_name}".strip(),
            image=image,
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=50)

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        user = authenticate(
            request=self.context["request"], username=email, password=password
        )

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": user,
        }


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "full_name", "image"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = USER_MODEL
        fields = ["id", "email", "profile"]


class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    code = serializers.CharField(write_only=True, required=True)
    message = serializers.CharField(read_only=True)

    def validate(self, attrs):
        user = USER_MODEL.objects.get(email=attrs["email"])
        if not user:
            raise InvalidRequest
        if user.is_verified:
            raise UserAlreadyVerified
        if not VerificationService.has_sent_verification_code(user.id):
            raise TokenExpired
        if VerificationService.has_attempt_exceeded(user.id):
            raise MaximumAttempt
        is_matched = VerificationService.check_verification_code(attrs["code"], user.id)
        if not is_matched:
            raise InvalidCode
        user.is_verified = True
        user.save()
        attrs["message"] = "Verified Successfully"
        return attrs


class ResendSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    message = serializers.CharField(read_only=True)

    def validate(self, attrs: Any) -> Any:
        email = attrs["email"]
        user = USER_MODEL.objects.get(email=email)
        if not user:
            raise serializers.ValidationError({"email": "User doesnot exist"})
        if user.is_verified:
            raise serializers.ValidationError("User already verified")
        already_resent, remaining_ttl = VerificationService.has_resend_key(user.id)

        if already_resent:
            raise serializers.ValidationError(f"Please wait {remaining_ttl} seconds")
        VerificationService.set_resend_key(user.id)
        send_verification_message.delay(user.id)
        attrs["message"] = "Resent code succesfully"
        return attrs


class ForgetSerializer(serializers.Serializer):
    email=serializers.EmailField(required=True)

    def validate(self, attrs):
        email=attrs["email"]
        user=get_object_or_404(USER_MODEL,email=email)
        token=default_token_generator.make_token(user)
        return {
            "token":token,
            "user_id":user.id
        }

class ResetSerializer(serializers.Serializer):
    token=serializers.CharField(required=True)
    uuid=serializers.UUIDField(required=True)
    new_password=serializers.CharField(write_only=True)
    def validate(self, attrs):
        user_id=attrs["uuid"]
        token=attrs["token"]
        new=attrs["new_password"]
        user=get_object_or_404(USER_MODEL,id=user_id)
        if not default_token_generator.check_token(token=token,user=user):
            raise InvalidOrExpiredToken
        user.set_password(new)
        user.save()


