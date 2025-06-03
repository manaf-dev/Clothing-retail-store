from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Inventory, Supplier, RestockHistory
from .serializers import (
    InventorySerializer,
    SupplierSerializer,
    RestockHistorySerializer,
)

# Create your views here.


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["product__name"]
    ordering_fields = ["stock", "min_stock"]


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class RestockHistoryViewSet(viewsets.ModelViewSet):
    queryset = RestockHistory.objects.all()
    serializer_class = RestockHistorySerializer
