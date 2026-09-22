from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .exceptions import InvalidUser
from .models import User


@admin.register(User)
class ModelAdmin(UserAdmin):
    list_display = ["__str__", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "email"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at", "updated_at"]
    date_hierarchy = "created_at"
    list_per_page = 25
    list_select_related = True
    save_on_top = True

    fieldsets = (
        ("General", {"fields": ("name",)}),
        ("Status", {"fields": ("is_active",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    @admin.action(description="Mark selected as active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    actions = ["make_active"]
