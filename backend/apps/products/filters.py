"""
Django filters for Product model.
Provides advanced filtering capabilities for the Product API.
"""

import django_filters
from django.db.models import Q
from .models import Product, Category


class ProductFilter(django_filters.FilterSet):
    """
    FilterSet for Product model with advanced filtering options.
    """

    # Search across multiple fields
    search = django_filters.CharFilter(method="filter_search", label="Search")

    # Category filtering
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(), field_name="category", label="Category"
    )

    # Price range filtering
    price_min = django_filters.NumberFilter(
        field_name="price", lookup_expr="gte", label="Minimum Price"
    )
    price_max = django_filters.NumberFilter(
        field_name="price", lookup_expr="lte", label="Maximum Price"
    )

    # Stock filtering
    stock_min = django_filters.NumberFilter(
        field_name="stock", lookup_expr="gte", label="Minimum Stock"
    )
    stock_max = django_filters.NumberFilter(
        field_name="stock", lookup_expr="lte", label="Maximum Stock"
    )

    # Stock status filtering
    stock_status = django_filters.ChoiceFilter(
        choices=[
            ("in_stock", "In Stock"),
            ("low_stock", "Low Stock"),
            ("out_of_stock", "Out of Stock"),
        ],
        method="filter_stock_status",
        label="Stock Status",
    )

    # Status filtering
    status = django_filters.ChoiceFilter(
        choices=Product.STATUS_CHOICES, field_name="status", label="Product Status"
    )

    # Date range filtering
    created_after = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte", label="Created After"
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte", label="Created Before"
    )

    # Sale items filtering
    on_sale = django_filters.BooleanFilter(method="filter_on_sale", label="On Sale")

    class Meta:
        model = Product
        fields = [
            "search",
            "category",
            "price_min",
            "price_max",
            "stock_min",
            "stock_max",
            "stock_status",
            "status",
            "created_after",
            "created_before",
            "on_sale",
        ]

    def filter_search(self, queryset, name, value):
        """
        Filter products by search term across multiple fields.
        """
        if not value:
            return queryset

        return queryset.filter(
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(category__name__icontains=value)
        )

    def filter_stock_status(self, queryset, name, value):
        """
        Filter products by stock status.
        """
        if value == "in_stock":
            return queryset.filter(stock__gt=10)
        elif value == "low_stock":
            return queryset.filter(stock__gt=0, stock__lte=10)
        elif value == "out_of_stock":
            return queryset.filter(stock=0)
        return queryset

    def filter_on_sale(self, queryset, name, value):
        """
        Filter products that are on sale.
        """
        if value:
            return queryset.filter(sale_price__isnull=False, sale_price__gt=0)
        else:
            return queryset.filter(Q(sale_price__isnull=True) | Q(sale_price=0))


class CategoryFilter(django_filters.FilterSet):
    """
    FilterSet for Category model.
    """

    search = django_filters.CharFilter(method="filter_search", label="Search")

    class Meta:
        model = Category
        fields = ["search"]

    def filter_search(self, queryset, name, value):
        """
        Filter categories by search term.
        """
        if not value:
            return queryset

        return queryset.filter(
            Q(name__icontains=value) | Q(description__icontains=value)
        )
