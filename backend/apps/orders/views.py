from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from datetime import date, datetime, timedelta
from django.utils import timezone
from django.db.models import Sum, Count, Avg
from decimal import Decimal

from .models import Order, OrderItem
from .serializers import (
    OrderReadSerializer,
    OrderWriteSerializer,
    OrderItemReadSerializer,
    SalesReportSerializer,
    WeeklySalesReportSerializer,
    MonthlySalesReportSerializer,
    TopProductSerializer,
    PaymentMethodReportSerializer,
)
from .selectors import OrderSelectors, SalesSelectors, OrderItemSelectors
from .services import OrderService, SalesAnalyticsService
from .filters import OrderFilter


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing orders and sales
    """

    queryset = Order.objects.all().prefetch_related("items__product")
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = OrderFilter
    search_fields = [
        "order_number",
        "customer_name",
        "served_by",
    ]
    ordering_fields = ["created_at", "total", "status", "order_number"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Use selectors for optimized queries"""
        return OrderSelectors.get_order_list()

    def perform_create(self, serializer):
        """Use service layer for order creation"""
        print("Creating order with data:", serializer.validated_data)
        # Let the serializer handle the creation since it's properly configured
        return serializer.save()

    def create(self, request, *args, **kwargs):
        """Override create to handle custom logic if needed"""
        print("Creating order with request data:", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        """Mark order as completed"""
        order = self.get_object()
        try:
            completed_order = OrderService.complete_order(order.id)
            serializer = self.get_serializer(completed_order)
            return Response(serializer.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """Cancel an order"""
        order = self.get_object()
        try:
            cancelled_order = OrderService.cancel_order(order.id)
            serializer = self.get_serializer(cancelled_order)
            return Response(serializer.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def refund(self, request, pk=None):
        """Process order refund"""
        order = self.get_object()
        try:
            refunded_order = OrderService.refund_order(order.id)
            serializer = self.get_serializer(refunded_order)
            return Response(serializer.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action in ["create", "update", "partial_update"]:
            return OrderWriteSerializer
        return OrderReadSerializer

    @action(detail=False, methods=["get"])
    def pending(self, request):
        """Get all pending orders using selectors"""
        pending_orders = OrderSelectors.get_pending_orders()
        page = self.paginate_queryset(pending_orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(pending_orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def recent(self, request):
        """Get recent orders using selectors"""
        limit = int(request.query_params.get("limit", 10))
        recent_orders = OrderSelectors.get_recent_orders(limit=limit)
        serializer = self.get_serializer(recent_orders, many=True)
        return Response(serializer.data)


class SalesAnalyticsViewSet(viewsets.ViewSet):
    """
    ViewSet for sales analytics and reporting using service layer
    """

    filter_backends = [DjangoFilterBackend]

    @action(detail=False, methods=["get"])
    def dashboard(self, request):
        """Get comprehensive sales dashboard data"""
        analytics_service = SalesAnalyticsService()

        # Get dashboard stats for different periods
        today_stats = analytics_service.get_dashboard_stats("today")
        week_stats = analytics_service.get_dashboard_stats("week")
        month_stats = analytics_service.get_dashboard_stats("month")

        return Response(
            {
                "today": today_stats,
                "this_week": week_stats,
                "this_month": month_stats,
                "timestamp": timezone.now(),
            }
        )

    @action(detail=False, methods=["get"])
    def daily_report(self, request):
        """Get daily sales report"""
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        analytics_service = SalesAnalyticsService()
        report_data = analytics_service.get_daily_sales_report(start_date, end_date)

        serializer = SalesReportSerializer(report_data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def weekly_report(self, request):
        """Get weekly sales report"""
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        analytics_service = SalesAnalyticsService()
        report_data = analytics_service.get_weekly_sales_report(start_date, end_date)

        serializer = WeeklySalesReportSerializer(report_data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def monthly_report(self, request):
        """Get monthly sales report"""
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        analytics_service = SalesAnalyticsService()
        report_data = analytics_service.get_monthly_sales_report(start_date, end_date)

        serializer = MonthlySalesReportSerializer(report_data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def top_products(self, request):
        """Get top selling products"""
        period = request.query_params.get("period", "month")  # day, week, month, year
        limit = int(request.query_params.get("limit", 10))

        analytics_service = SalesAnalyticsService()
        top_products = analytics_service.get_top_products(period=period, limit=limit)

        serializer = TopProductSerializer(top_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def payment_methods(self, request):
        """Get payment method breakdown"""
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        # If no dates provided, use default month period
        if not start_date or not end_date:
            from datetime import date, timedelta
            from django.utils import timezone

            today = timezone.now().date()
            end_date = today
            start_date = today.replace(day=1)  # First day of current month
        else:
            # Convert string dates to date objects
            from datetime import datetime

            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        analytics_service = SalesAnalyticsService()
        payment_data = analytics_service.get_payment_method_stats(
            start_date=start_date, end_date=end_date
        )

        serializer = PaymentMethodReportSerializer(payment_data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def trends(self, request):
        """Get sales trends over time"""
        period = request.query_params.get("period", "daily")  # daily, weekly, monthly
        days = int(request.query_params.get("days", 30))

        analytics_service = SalesAnalyticsService()
        trends_data = analytics_service.get_sales_trends(period=period, days=days)

        return Response(trends_data)

    @action(detail=False, methods=["get"])
    def customer_stats(self, request):
        """Get customer-related sales statistics"""
        period = request.query_params.get("period", "month")

        selectors = SalesSelectors()
        customer_stats = selectors.get_customer_stats(period=period)

        return Response(customer_stats)


class OrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly ViewSet for order items using selectors
    """

    serializer_class = OrderItemReadSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["product_name", "product__name"]
    ordering_fields = ["quantity", "price", "order__created_at"]
    ordering = ["-order__created_at"]

    def get_queryset(self):
        """Use selectors for optimized queries"""
        return OrderItemSelectors.list_order_items()
