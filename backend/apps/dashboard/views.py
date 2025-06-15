from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count, Avg, F
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from apps.orders.models import Order, OrderItem
from apps.products.models import Product
from apps.inventory.models import Inventory


@api_view(["GET"])
def dashboard_overview(request):
    """
    Comprehensive dashboard API for in-store management system
    Returns key metrics for today, week, month, and overall
    """

    # Get date ranges
    today = timezone.now().date()
    # week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    print(f"Today's date: {today}, Month start: {month_start}")

    # Today's metrics
    today_orders = Order.objects.filter(
        created_at__date=today, status__in=["completed", "paid"]
    )
    today_metrics = {
        "orders_count": today_orders.count(),
        "total_sales": today_orders.aggregate(total=Sum("total"))["total"]
        or Decimal("0"),
        "avg_order_value": today_orders.aggregate(avg=Avg("total"))["avg"]
        or Decimal("0"),
        "items_sold": OrderItem.objects.filter(order__in=today_orders).aggregate(
            total=Sum("quantity")
        )["total"]
        or 0,
    }

    # This week's metrics
    # week_orders = Order.objects.filter(
    #     created_at__date__gte=week_start, status__in=["completed", "paid"]
    # )
    # week_metrics = {
    #     "orders_count": week_orders.count(),
    #     "total_sales": week_orders.aggregate(total=Sum("total"))["total"]
    #     or Decimal("0"),
    #     "avg_order_value": week_orders.aggregate(avg=Avg("total"))["avg"]
    #     or Decimal("0"),
    #     "items_sold": OrderItem.objects.filter(order__in=week_orders).aggregate(
    #         total=Sum("quantity")
    #     )["total"]
    #     or 0,
    # }

    # This month's metrics
    month_orders = Order.objects.filter(
        created_at__date__gte=month_start, status__in=["completed", "paid"]
    )
    month_metrics = {
        "orders_count": month_orders.count(),
        "total_revenue": month_orders.aggregate(total=Sum("total"))["total"]
        or Decimal("0"),
        "avg_order_value": month_orders.aggregate(avg=Avg("total"))["avg"]
        or Decimal("0"),
        "items_sold": OrderItem.objects.filter(order__in=month_orders).aggregate(
            total=Sum("quantity")
        )["total"]
        or 0,
    }

    # Inventory status
    # total_products = Product.objects.filter(status="active").count()
    # low_stock_products = Product.objects.filter(status="active", stock__lte=10).count()
    # out_of_stock_products = Product.objects.filter(status="active", stock=0).count()

    # Top selling products (this month)
    # top_products = (
    #     OrderItem.objects.filter(
    #         order__created_at__date__gte=month_start,
    #         order__status__in=["completed", "paid"],
    #     )
    #     .values("product__name", "product_name")
    #     .annotate(
    #         total_quantity=Sum("quantity"),
    #         total_revenue=Sum(F("quantity") * F("price")),
    #     )
    #     .order_by("-total_quantity")[:5]
    # )

    # Inventory alerts
    low_stock_products = (
        Product.objects.filter(status="active", stock__lte=10)
        .values("id", "name", "stock", "min_stock")
        .order_by("stock")[:5]
    )

    # inventory_alerts = {
    #     "low_stock_items": list(low_stock_products),
    # }

    # Recent orders
    recent_orders = (
        Order.objects.select_related()
        .prefetch_related("items__product")
        .order_by("-created_at")[:10]
    )

    recent_orders_data = []
    for order in recent_orders:
        recent_orders_data.append(
            {
                "id": str(order.id),
                "order_number": order.order_number,
                "customer_name": order.customer_name,
                "total": str(order.total),
                "status": order.status,
                "payment_method": order.payment_method,
                "created_at": order.created_at.isoformat(),
                "items_count": order.items.count(),
            }
        )

    context = {
        "month_metrics": month_metrics,
        "today_metrics": today_metrics,
        "recent_orders": recent_orders_data,
        "inventory_alerts": list(low_stock_products),
    }

    return Response(context, status=status.HTTP_200_OK)


@api_view(["GET"])
def sales_summary(request):
    """
    Quick sales summary for the current day
    """
    today = timezone.now().date()

    # Today's completed orders
    today_orders = Order.objects.filter(
        created_at__date=today, status__in=["completed", "paid"]
    )

    summary = {
        "date": today.isoformat(),
        "total_orders": today_orders.count(),
        "total_sales": str(
            today_orders.aggregate(total=Sum("total"))["total"] or Decimal("0")
        ),
        "total_items": OrderItem.objects.filter(order__in=today_orders).aggregate(
            total=Sum("quantity")
        )["total"]
        or 0,
        "pending_orders": Order.objects.filter(
            created_at__date=today, status="pending"
        ).count(),
        "cash_sales": str(
            today_orders.filter(payment_method="cash").aggregate(total=Sum("total"))[
                "total"
            ]
            or Decimal("0")
        ),
        "card_sales": str(
            today_orders.filter(payment_method="card").aggregate(total=Sum("total"))[
                "total"
            ]
            or Decimal("0")
        ),
    }

    return Response(summary)


@api_view(["GET"])
def inventory_alerts(request):
    """
    Get inventory alerts for low stock and out of stock items
    """

    # Low stock products (stock <= 10)
    low_stock = (
        Product.objects.filter(status="active", stock__lte=10, stock__gt=0)
        .values("id", "name", "stock", "min_stock")
        .order_by("stock")
    )

    # Out of stock products
    out_of_stock = Product.objects.filter(status="active", stock=0).values(
        "id", "name", "stock", "min_stock"
    )

    return Response(
        {
            "low_stock_products": list(low_stock),
            "out_of_stock_products": list(out_of_stock),
            "low_stock_count": low_stock.count(),
            "out_of_stock_count": out_of_stock.count(),
        }
    )
