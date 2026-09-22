from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "is_active", "is_staff", "created_at")
    search_fields = ("email",)
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),

    )
    # override add_fieldsets (remove username)
    add_fieldsets = (
        (None, {
            "fields": ("email", "password1", "password2", "is_active", "is_staff", "is_superuser"),
        }),
    )
