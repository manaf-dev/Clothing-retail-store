from typing import Optional, List, Dict
from datetime import date, datetime, timedelta
from django.db.models import QuerySet, Q, Prefetch
from django.utils import timezone
from .models import Order, OrderItem


class OrderSelectors:
    """Selectors for order queries"""

    @staticmethod
    def get_order_list(
        status: Optional[str] = None,
        payment_status: Optional[str] = None,
        payment_method: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        search: Optional[str] = None,
        served_by: Optional[str] = None,
    ) -> QuerySet[Order]:
        """
        Get filtered order list with optimized queries
        """
        queryset = Order.objects.prefetch_related(
            Prefetch("items", queryset=OrderItem.objects.select_related("product"))
        )

        # Apply filters
        if status:
            queryset = queryset.filter(status=status)
        if payment_status:
            queryset = queryset.filter(payment_status=payment_status)
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
        if served_by:
            queryset = queryset.filter(served_by__icontains=served_by)
        if search:
            queryset = queryset.filter(
                Q(order_number__icontains=search)
                | Q(customer_name__icontains=search)
                | Q(served_by__icontains=search)
            )

        return queryset.order_by("-created_at")

    @staticmethod
    def get_pending_orders() -> QuerySet[Order]:
        """Get all pending orders"""
        return (
            Order.objects.filter(status="pending")
            .prefetch_related("items__product")
            .order_by("created_at")
        )

    @staticmethod
    def get_recent_orders(limit: int = 10) -> QuerySet[Order]:
        """Get recent orders"""
        return Order.objects.prefetch_related("items__product").order_by("-created_at")[
            :limit
        ]


class SalesSelectors:
    """Selectors for sales analytics queries"""

    @staticmethod
    def get_sales_orders(
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        status: str = "completed",
    ) -> QuerySet[Order]:
        """
        Get sales orders for analytics

        Args:
            start_date: Start date filter
            end_date: End date filter
            status: Order status (default: completed)

        Returns:
            QuerySet of sales orders
        """
        queryset = Order.objects.filter(status=status)

        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)

        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)

        return queryset.select_related("customer").prefetch_related("items__product")

    @staticmethod
    def get_todays_sales() -> QuerySet[Order]:
        """
        Get today's completed sales

        Returns:
            QuerySet of today's sales
        """
        today = timezone.now().date()
        return (
            Order.objects.filter(status="completed", created_at__date=today)
            .select_related("customer")
            .prefetch_related("items__product")
        )

    @staticmethod
    def get_weekly_sales(weeks_back: int = 0) -> QuerySet[Order]:
        """
        Get weekly sales (current week or previous weeks)

        Args:
            weeks_back: Number of weeks back from current week (0 = current week)

        Returns:
            QuerySet of weekly sales
        """
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday() + (weeks_back * 7))
        end_of_week = start_of_week + timedelta(days=6)

        return (
            Order.objects.filter(
                status="completed", created_at__date__range=[start_of_week, end_of_week]
            )
            .select_related("customer")
            .prefetch_related("items__product")
        )

    @staticmethod
    def get_monthly_sales(year: int, month: int) -> QuerySet[Order]:
        """
        Get monthly sales for a specific year and month

        Args:
            year: Year
            month: Month (1-12)

        Returns:
            QuerySet of monthly sales
        """
        return (
            Order.objects.filter(
                status="completed", created_at__year=year, created_at__month=month
            )
            .select_related("customer")
            .prefetch_related("items__product")
        )

    @staticmethod
    def get_high_value_orders(min_amount: float = 1000.0) -> QuerySet[Order]:
        """
        Get high-value orders above a certain threshold

        Args:
            min_amount: Minimum order amount

        Returns:
            QuerySet of high-value orders
        """
        return (
            Order.objects.filter(status="completed", total__gte=min_amount)
            .select_related("customer")
            .prefetch_related("items__product")
            .order_by("-total")
        )

    @staticmethod
    def get_refunded_orders(
        start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> QuerySet[Order]:
        """
        Get refunded orders

        Args:
            start_date: Start date filter
            end_date: End date filter

        Returns:
            QuerySet of refunded orders
        """
        queryset = Order.objects.filter(status="refunded")

        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)

        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)

        return queryset.select_related("customer").prefetch_related("items__product")


class OrderItemSelectors:
    """Selectors for order item queries"""

    @staticmethod
    def get_popular_products(
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: int = 10,
    ) -> QuerySet[OrderItem]:
        """
        Get popular products based on order items

        Args:
            start_date: Start date filter
            end_date: End date filter
            limit: Number of products to return

        Returns:
            QuerySet of order items grouped by product
        """
        queryset = OrderItem.objects.filter(order__status="completed")

        if start_date:
            queryset = queryset.filter(order__created_at__date__gte=start_date)

        if end_date:
            queryset = queryset.filter(order__created_at__date__lte=end_date)

        return queryset.select_related("product", "order").order_by("-quantity")[:limit]

    @staticmethod
    def get_product_sales_history(
        product_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> QuerySet[OrderItem]:
        """
        Get sales history for a specific product

        Args:
            product_id: Product ID
            start_date: Start date filter
            end_date: End date filter

        Returns:
            QuerySet of order items for the product
        """
        queryset = OrderItem.objects.filter(
            product_id=product_id, order__status="completed"
        )

        if start_date:
            queryset = queryset.filter(order__created_at__date__gte=start_date)

        if end_date:
            queryset = queryset.filter(order__created_at__date__lte=end_date)

        return queryset.select_related("order").order_by("-order__created_at")
