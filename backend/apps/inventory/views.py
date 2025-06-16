from django.shortcuts import render
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, F
from .models import Inventory, Supplier, RestockHistory
from .serializers import (
    InventorySerializer,
    SupplierSerializer,
    RestockHistorySerializer,
)

# Create your views here.


class InventoryViewSet(viewsets.ViewSet):
    """
    ViewSet for handling inventory operations.
    Provides CRUD operations with filtering, searching, and pagination.
    """

    def list(self, request):
        """
        List all inventory items with filtering, searching, and pagination.

        Query Parameters:
        - search: Search term for product name/SKU
        - category: Category name
        - stock_status: good, low, out
        - ordering: Field to order by
        - page: Page number
        - page_size: Items per page (default: 10)
        """
        # Get query parameters
        search = request.query_params.get("search", None)
        category = request.query_params.get("category", None)
        stock_status = request.query_params.get("stock_status", None)
        ordering = request.query_params.get("ordering", "-created_at")
        page = request.query_params.get("page", 1)
        page_size = int(request.query_params.get("page_size", 10))

        # Start with base queryset
        queryset = Inventory.objects.select_related(
            "product", "product__category", "supplier"
        ).all()

        # Apply filters
        if search:
            queryset = queryset.filter(
                Q(product__name__icontains=search) | Q(product__sku__icontains=search)
            )

        if category and category != "all":
            queryset = queryset.filter(product__category__name__icontains=category)

        if stock_status and stock_status != "all":
            if stock_status == "low":
                queryset = queryset.filter(stock__lte=F("min_stock"))
            elif stock_status == "out":
                queryset = queryset.filter(stock=0)
            elif stock_status == "good":
                queryset = queryset.filter(stock__gt=F("min_stock"))

        # Apply ordering
        if ordering:
            queryset = queryset.order_by(ordering)

        # Pagination
        paginator = Paginator(queryset, page_size)
        try:
            inventory_page = paginator.page(page)
        except PageNotAnInteger:
            inventory_page = paginator.page(1)
        except EmptyPage:
            inventory_page = paginator.page(paginator.num_pages)

        # Serialize data
        serializer = InventorySerializer(inventory_page, many=True)

        return Response(
            {
                "results": serializer.data,
                "count": paginator.count,
                "num_pages": paginator.num_pages,
                "current_page": inventory_page.number,
                "has_next": inventory_page.has_next(),
                "has_previous": inventory_page.has_previous(),
            },
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, pk=None):
        """Retrieve a specific inventory item by ID."""
        try:
            inventory = Inventory.objects.select_related(
                "product", "product__category", "supplier"
            ).get(pk=pk)
            serializer = InventorySerializer(inventory)
            return Response(serializer.data)
        except Inventory.DoesNotExist:
            return Response(
                {"error": "Inventory item not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def update(self, request, pk=None):
        """Update a specific inventory item."""
        try:
            inventory = Inventory.objects.get(pk=pk)
        except Inventory.DoesNotExist:
            return Response(
                {"error": "Inventory item not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Handle stock_quantity update
        if "stock_quantity" in request.data:
            new_stock = request.data.get("stock_quantity")
            try:
                new_stock = int(new_stock)
                if new_stock < 0:
                    return Response(
                        {"error": "Stock quantity cannot be negative"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                inventory.stock = new_stock
                inventory.save()

                # Also update the product stock
                inventory.product.stock = new_stock
                inventory.product.save()

                serializer = InventorySerializer(inventory)
                return Response(serializer.data)

            except (ValueError, TypeError):
                return Response(
                    {"error": "Invalid stock quantity"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Handle other field updates
        serializer = InventorySerializer(inventory, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def low_stock(self, request):
        """Get items with low stock"""
        queryset = Inventory.objects.select_related(
            "product", "product__category", "supplier"
        ).filter(stock__lte=F("min_stock"))

        serializer = InventorySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def out_of_stock(self, request):
        """Get items that are out of stock"""
        queryset = Inventory.objects.select_related(
            "product", "product__category", "supplier"
        ).filter(stock=0)

        serializer = InventorySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def update_stock(self, request, pk=None):
        """Update stock quantity for a specific inventory item"""
        try:
            inventory = Inventory.objects.get(pk=pk)
        except Inventory.DoesNotExist:
            return Response(
                {"error": "Inventory item not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        new_stock = request.data.get("stock")
        if new_stock is None:
            return Response(
                {"error": "Stock quantity is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            new_stock = int(new_stock)
            if new_stock < 0:
                return Response(
                    {"error": "Stock quantity cannot be negative"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            inventory.stock = new_stock
            inventory.save()

            # Also update the product stock
            inventory.product.stock = new_stock
            inventory.product.save()

            serializer = InventorySerializer(inventory)
            return Response(serializer.data)

        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid stock quantity"}, status=status.HTTP_400_BAD_REQUEST
            )


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "email", "phone"]
    ordering = ["name"]


class RestockHistoryViewSet(viewsets.ModelViewSet):
    queryset = RestockHistory.objects.select_related("inventory", "supplier").all()
    serializer_class = RestockHistorySerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ["-restocked_at"]
