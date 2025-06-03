from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import InventoryViewSet, SupplierViewSet, RestockHistoryViewSet

router = DefaultRouter()
router.register(r"", InventoryViewSet, basename="inventory")
router.register(r"suppliers", SupplierViewSet, basename="supplier")
router.register(r"restock-history", RestockHistoryViewSet, basename="restockhistory")

urlpatterns = router.urls
