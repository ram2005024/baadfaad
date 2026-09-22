from django.urls import path

from apps.user.views import RegisterView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="user_register"),
]
