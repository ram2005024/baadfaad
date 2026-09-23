from django.urls import path

from apps.user.views import RegisterView, LoginView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="user_register"),
    path("auth/login/", LoginView.as_view(), name="user_login"),
]
