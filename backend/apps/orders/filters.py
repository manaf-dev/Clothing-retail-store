import django_filters
from django_filters import rest_framework as filters
from django.db import models
from .models import Order, OrderItem


class OrderFilter(filters.FilterSet):
    """Filter class for Order model"""

    # Date range filters
    created_after = filters.DateFilter(field_name="created_at", lookup_expr="date__gte")
    created_before = filters.DateFilter(
        field_name="created_at", lookup_expr="date__lte"
    )
    created_range = filters.DateFromToRangeFilter(field_name="created_at__date")

    # Amount range filters
    total_min = filters.NumberFilter(field_name="total", lookup_expr="gte")
    total_max = filters.NumberFilter(field_name="total", lookup_expr="lte")
    total_range = filters.RangeFilter(field_name="total")

    # Status filters
    status = filters.ChoiceFilter(choices=Order.STATUS_CHOICES)
    payment_status = filters.ChoiceFilter(
        choices=[
            ("pending", "Pending"),
            ("paid", "Paid"),
            ("partially_paid", "Partially Paid"),
            ("failed", "Failed"),
            ("refunded", "Refunded"),
        ]
    )
    payment_method = filters.ChoiceFilter(choices=Order.PAYMENT_METHODS)

    # Customer filter
    customer = filters.UUIDFilter(field_name="customer__id")
    customer_name = filters.CharFilter(
        field_name="customer__name", lookup_expr="icontains"
    )
    customer_email = filters.CharFilter(
        field_name="customer__email", lookup_expr="icontains"
    )
    customer_phone = filters.CharFilter(
        field_name="customer__phone", lookup_expr="icontains"
    )

    # Order number filter
    order_number = filters.CharFilter(lookup_expr="icontains")

    # Staff filter
    served_by = filters.CharFilter(lookup_expr="icontains")

    # Has customer filter
    has_customer = filters.BooleanFilter(
        field_name="customer", lookup_expr="isnull", exclude=True, label="Has Customer"
    )

    # Today's orders
    today = filters.BooleanFilter(method="filter_today", label="Today's Orders")

    # This week's orders
    this_week = filters.BooleanFilter(
        method="filter_this_week", label="This Week's Orders"
    )

    # This month's orders
    this_month = filters.BooleanFilter(
        method="filter_this_month", label="This Month's Orders"
    )

    class Meta:
        model = Order
        fields = {
            "status": ["exact"],
            "payment_status": ["exact"],
            "payment_method": ["exact"],
            "total": ["gte", "lte", "exact"],
            "created_at": ["gte", "lte", "exact"],
            "updated_at": ["gte", "lte"],
        }

    def filter_today(self, queryset, name, value):
        """Filter orders created today"""
        if value:
            from django.utils import timezone

            today = timezone.now().date()
            return queryset.filter(created_at__date=today)
        return queryset

    def filter_this_week(self, queryset, name, value):
        """Filter orders created this week"""
        if value:
            from django.utils import timezone
            from datetime import timedelta

            today = timezone.now().date()
            start_of_week = today - timedelta(days=today.weekday())
            return queryset.filter(created_at__date__gte=start_of_week)
        return queryset

    def filter_this_month(self, queryset, name, value):
        """Filter orders created this month"""
        if value:
            from django.utils import timezone

            today = timezone.now().date()
            return queryset.filter(
                created_at__year=today.year, created_at__month=today.month
            )
        return queryset


class OrderItemFilter(filters.FilterSet):
    """Filter class for OrderItem model"""

    # Product filters
    product = filters.UUIDFilter(field_name="product__id")
    product_name = filters.CharFilter(lookup_expr="icontains")
    product_category = filters.UUIDFilter(field_name="product__category__id")

    # Quantity filters
    quantity_min = filters.NumberFilter(field_name="quantity", lookup_expr="gte")
    quantity_max = filters.NumberFilter(field_name="quantity", lookup_expr="lte")

    # Price filters
    price_min = filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = filters.NumberFilter(field_name="price", lookup_expr="lte")

    # Order filters
    order_status = filters.ChoiceFilter(
        field_name="order__status", choices=Order.STATUS_CHOICES
    )
    order_created_after = filters.DateFilter(
        field_name="order__created_at", lookup_expr="date__gte"
    )
    order_created_before = filters.DateFilter(
        field_name="order__created_at", lookup_expr="date__lte"
    )

    # Discount filter
    has_discount = filters.BooleanFilter(
        field_name="discount", lookup_expr="gt", label="Has Discount"
    )

    class Meta:
        model = OrderItem
        fields = {
            "quantity": ["gte", "lte", "exact"],
            "price": ["gte", "lte", "exact"],
            "discount": ["gte", "lte", "exact"],
        }


class SalesReportFilter(filters.FilterSet):
    """Filter class for sales reporting"""

    # Date range for reports
    start_date = filters.DateFilter(method="filter_start_date")
    end_date = filters.DateFilter(method="filter_end_date")

    # Predefined periods
    period = filters.ChoiceFilter(
        choices=[
            ("today", "Today"),
            ("yesterday", "Yesterday"),
            ("this_week", "This Week"),
            ("last_week", "Last Week"),
            ("this_month", "This Month"),
            ("last_month", "Last Month"),
            ("this_year", "This Year"),
            ("last_year", "Last Year"),
        ],
        method="filter_period",
    )

    # Product category for analysis
    category = filters.UUIDFilter(field_name="items__product__category__id")

    # Payment method for analysis
    payment_method = filters.ChoiceFilter(choices=Order.PAYMENT_METHODS)

    # Minimum order value
    min_order_value = filters.NumberFilter(field_name="total", lookup_expr="gte")

    def filter_start_date(self, queryset, name, value):
        """Filter by start date"""
        if value:
            return queryset.filter(created_at__date__gte=value)
        return queryset

    def filter_end_date(self, queryset, name, value):
        """Filter by end date"""
        if value:
            return queryset.filter(created_at__date__lte=value)
        return queryset

    def filter_period(self, queryset, name, value):
        """Filter by predefined period"""
        from django.utils import timezone
        from datetime import timedelta

        today = timezone.now().date()

        if value == "today":
            return queryset.filter(created_at__date=today)
        elif value == "yesterday":
            yesterday = today - timedelta(days=1)
            return queryset.filter(created_at__date=yesterday)
        elif value == "this_week":
            start_of_week = today - timedelta(days=today.weekday())
            return queryset.filter(created_at__date__gte=start_of_week)
        elif value == "last_week":
            start_of_last_week = today - timedelta(days=today.weekday() + 7)
            end_of_last_week = start_of_last_week + timedelta(days=6)
            return queryset.filter(
                created_at__date__range=[start_of_last_week, end_of_last_week]
            )
        elif value == "this_month":
            return queryset.filter(
                created_at__year=today.year, created_at__month=today.month
            )
        elif value == "last_month":
            if today.month == 1:
                last_month_year = today.year - 1
                last_month = 12
            else:
                last_month_year = today.year
                last_month = today.month - 1
            return queryset.filter(
                created_at__year=last_month_year, created_at__month=last_month
            )
        elif value == "this_year":
            return queryset.filter(created_at__year=today.year)
        elif value == "last_year":
            return queryset.filter(created_at__year=today.year - 1)

        return queryset

    class Meta:
        model = Order
        fields = []
