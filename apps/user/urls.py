from django.urls import path

from apps.user.views import (
    LoginView,
    MeView,
    RefreshView,
    RegisterView,
    ResendView,
    VerifyView, PasswordForgetView, PasswordResetView,
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="user_register"),
    path("auth/login/", LoginView.as_view(), name="user_login"),
    path("auth/refresh/", RefreshView.as_view(), name="user_refresh"),
    path("auth/me/", MeView.as_view(), name="user_refresh"),
    path("auth/verify/", VerifyView.as_view(), name="user_verify"),
    path("auth/resend/", ResendView.as_view(), name="user_resend"),
    path("auth/forget/", PasswordForgetView.as_view(), name="user_forget"),
    path("auth/reset/", PasswordResetView.as_view(), name="user_reset"),
]
