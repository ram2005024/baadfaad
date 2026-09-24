from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.user.exceptions import InvalidUser
from common.base_model import BaseModel


class CustomBaseUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")

        email = self.normalize_email(email)

        if self.model.objects.filter(email=email).exists():
            raise InvalidUser("User with this email already exists")

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    username = None
    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomBaseUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"


class Profile(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.DB_CASCADE, related_name="profile"
    )
    image = models.ImageField(upload_to="profiles/", null=True, blank=True)
    full_name = models.CharField(max_length=200)
