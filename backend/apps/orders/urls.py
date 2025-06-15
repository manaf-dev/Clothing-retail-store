from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet, SalesAnalyticsViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r"sales/analytics", SalesAnalyticsViewSet, basename="sales-analytics")
router.register(r"items", OrderItemViewSet, basename="orderitem")
router.register(r"", OrderViewSet, basename="order")

urlpatterns = [
    # Include router URLs
    path("", include(router.urls)),
]
