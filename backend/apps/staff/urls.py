from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StaffViewSet

router = DefaultRouter()
router.register(r"", StaffViewSet, basename="staff")

urlpatterns = router.urls
