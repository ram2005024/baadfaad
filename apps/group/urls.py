from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.group.views import GroupViewSet

router=DefaultRouter()
router.register(r"groups",GroupViewSet,basename="group")

urlpatterns=[
    path("",include(router.urls))
]