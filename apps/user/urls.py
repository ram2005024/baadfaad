from django.urls import path

from apps.user.views import RegisterView, LoginView, RefreshView,MeView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="user_register"),
    path("auth/login/", LoginView.as_view(), name="user_login"),
    path("auth/refresh/", RefreshView.as_view(), name="user_refresh"),
    path("auth/me/", MeView.as_view(), name="user_refresh"),
]
