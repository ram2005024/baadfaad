from django.urls import path

from .views import UserDetailView, UserListView

urlpatterns = [
    path("list/", UserListView.as_view(), name="user-list"),
    path("detail/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
]
