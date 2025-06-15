from typing import Dict, List, Optional, Tuple, Any
from decimal import Decimal
from datetime import datetime, date, timedelta
from django.db import transaction
from django.db.models import Sum, Count, Avg, Q, F
from django.utils import timezone
from .models import Order, OrderItem
from apps.products.models import Product
from apps.customers.models import Customer


class OrderService:
    """Service class for order/sales operations"""

    @staticmethod
    @transaction.atomic
    def create_order(
        items: List[Dict],
        payment_method: str,
        customer_id: Optional[str] = None,
        payment_status: str = "pending",
        tax_amount: Decimal = Decimal("0"),
        discount_amount: Decimal = Decimal("0"),
        notes: str = "",
        served_by: str = "",
    ) -> Order:
        """
        Create a new order with items

        Args:
            items: List of dicts with product_id, quantity, price (optional), discount (optional)
            payment_method: Payment method used
            customer_id: Optional customer ID
            payment_status: Payment status
            tax_amount: Tax amount
            discount_amount: Discount amount
            notes: Order notes
            served_by: Staff member who served the order

        Returns:
            Created Order instance

        Raises:
            ValueError: If validation fails
        """
        if not items:
            raise ValueError("Order must contain at least one item")

        # Validate customer if provided
        customer = None
        if customer_id:
            try:
                customer = Customer.objects.get(id=customer_id)
            except Customer.DoesNotExist:
                raise ValueError("Customer does not exist")

        # Create order
        order = Order.objects.create(
            customer=customer,
            payment_method=payment_method,
            payment_status=payment_status,
            tax_amount=tax_amount,
            discount_amount=discount_amount,
            notes=notes,
            served_by=served_by,
        )

        # Process items
        subtotal = Decimal("0")
        for item_data in items:
            try:
                product = Product.objects.get(id=item_data["product_id"])
            except Product.DoesNotExist:
                raise ValueError(
                    f"Product with ID {item_data['product_id']} does not exist"
                )

            quantity = item_data["quantity"]
            if quantity <= 0:
                raise ValueError("Quantity must be greater than 0")

            # Check stock availability
            if product.stock < quantity:
                raise ValueError(
                    f"Insufficient stock for {product.name}. Available: {product.stock}, Requested: {quantity}"
                )

            # Use current product price if not provided
            price = Decimal(str(item_data.get("price", product.effective_price)))
            discount = Decimal(str(item_data.get("discount", 0)))

            # Create order item
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                quantity=quantity,
                price=price,
                discount=discount,
            )

            # Update product stock
            product.stock -= quantity
            product.save(update_fields=["stock"])

            subtotal += order_item.line_total

        # Update order totals
        order.subtotal = subtotal
        order.total = order.subtotal + order.tax_amount - order.discount_amount
        order.save(update_fields=["subtotal", "total"])

        return order

    @staticmethod
    def complete_order(order_id: str, payment_status: str = "paid") -> Order:
        """
        Mark an order as completed

        Args:
            order_id: Order ID
            payment_status: Payment status to set

        Returns:
            Updated Order instance
        """
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise ValueError("Order does not exist")

        if order.status == "completed":
            raise ValueError("Order is already completed")

        order.status = "completed"
        order.payment_status = payment_status
        order.completed_at = timezone.now()
        order.save(update_fields=["status", "payment_status", "completed_at"])

        return order

    @staticmethod
    @transaction.atomic
    def cancel_order(order_id: str, reason: str = "") -> Order:
        """
        Cancel an order and restore stock

        Args:
            order_id: Order ID
            reason: Cancellation reason

        Returns:
            Updated Order instance
        """
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise ValueError("Order does not exist")

        if order.status in ["completed", "cancelled"]:
            raise ValueError(f"Cannot cancel order with status: {order.status}")

        # Restore stock for each item
        for item in order.items.all():
            if item.product:
                item.product.stock += item.quantity
                item.product.save(update_fields=["stock"])

        # Update order
        order.status = "cancelled"
        if reason:
            order.notes = f"{order.notes}\n\nCancelled: {reason}".strip()
        order.save(update_fields=["status", "notes"])

        return order

    @staticmethod
    @transaction.atomic
    def refund_order(
        order_id: str, refund_amount: Optional[Decimal] = None, reason: str = ""
    ) -> Order:
        """
        Process a refund for an order

        Args:
            order_id: Order ID
            refund_amount: Amount to refund (defaults to full order total)
            reason: Refund reason

        Returns:
            Updated Order instance
        """
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise ValueError("Order does not exist")

        if order.status != "completed":
            raise ValueError("Can only refund completed orders")

        if refund_amount is None:
            refund_amount = order.total

        if refund_amount > order.total:
            raise ValueError("Refund amount cannot exceed order total")

        # Restore stock if full refund
        if refund_amount == order.total:
            for item in order.items.all():
                if item.product:
                    item.product.stock += item.quantity
                    item.product.save(update_fields=["stock"])

        # Update order
        order.status = "refunded"
        order.payment_status = "refunded"
        if reason:
            order.notes = f"{order.notes}\n\nRefunded {refund_amount}: {reason}".strip()
        order.save(update_fields=["status", "payment_status", "notes"])

        return order


class SalesAnalyticsService:
    """Service class for sales analytics and reporting"""

    @staticmethod
    def get_daily_sales(start_date: date, end_date: date) -> List[Dict]:
        """
        Get daily sales data for a date range

        Args:
            start_date: Start date
            end_date: End date

        Returns:
            List of daily sales data
        """
        sales_data = []
        current_date = start_date

        while current_date <= end_date:
            orders = Order.objects.filter(
                status="completed", created_at__date=current_date
            )

            daily_stats = orders.aggregate(
                total_sales=Sum("total") or Decimal("0"),
                total_orders=Count("id"),
                total_items=Sum("items__quantity") or 0,
                avg_order_value=Avg("total") or Decimal("0"),
            )

            sales_data.append(
                {
                    "date": current_date,
                    "total_sales": daily_stats["total_sales"],
                    "total_orders": daily_stats["total_orders"],
                    "total_items_sold": daily_stats["total_items"],
                    "average_order_value": daily_stats["avg_order_value"],
                }
            )

            current_date += timedelta(days=1)

        return sales_data

    @staticmethod
    def get_sales_summary(start_date: date, end_date: date) -> Dict:
        """
        Get sales summary for a date range

        Args:
            start_date: Start date
            end_date: End date

        Returns:
            Sales summary data
        """
        orders = Order.objects.filter(
            status="completed", created_at__date__range=[start_date, end_date]
        )

        summary = orders.aggregate(
            total_revenue=Sum("total") or Decimal("0"),
            total_orders=Count("id"),
            total_items_sold=Sum("items__quantity") or 0,
            average_order_value=Avg("total") or Decimal("0"),
            total_customers=Count("customer", distinct=True),
        )

        # Add comparison with previous period
        period_days = (end_date - start_date).days + 1
        prev_start = start_date - timedelta(days=period_days)
        prev_end = start_date - timedelta(days=1)

        prev_orders = Order.objects.filter(
            status="completed", created_at__date__range=[prev_start, prev_end]
        )

        prev_summary = prev_orders.aggregate(
            prev_revenue=Sum("total") or Decimal("0"),
            prev_orders=Count("id"),
            prev_items=Sum("items__quantity") or 0,
        )

        # Calculate growth percentages
        revenue_growth = 0
        if prev_summary["prev_revenue"] > 0:
            revenue_growth = (
                (summary["total_revenue"] - prev_summary["prev_revenue"])
                / prev_summary["prev_revenue"]
            ) * 100

        orders_growth = 0
        if prev_summary["prev_orders"] > 0:
            orders_growth = (
                (summary["total_orders"] - prev_summary["prev_orders"])
                / prev_summary["prev_orders"]
            ) * 100

        return {
            **summary,
            "revenue_growth_percentage": revenue_growth,
            "orders_growth_percentage": orders_growth,
            "period_start": start_date,
            "period_end": end_date,
        }

    @staticmethod
    def get_top_products(
        start_date: date, end_date: date, limit: int = 10
    ) -> List[Dict]:
        """
        Get top-selling products for a date range

        Args:
            start_date: Start date
            end_date: End date
            limit: Number of products to return

        Returns:
            List of top products data
        """
        from django.db.models import Sum, Count

        top_products = (
            OrderItem.objects.filter(
                order__status="completed",
                order__created_at__date__range=[start_date, end_date],
            )
            .values("product_id", "product_name")
            .annotate(
                total_quantity=Sum("quantity"),
                total_revenue=Sum(F("quantity") * F("price") - F("discount")),
                order_count=Count("order", distinct=True),
            )
            .order_by("-total_revenue")[:limit]
        )

        return list(top_products)

    @staticmethod
    def get_payment_method_stats(start_date: date, end_date: date) -> List[Dict]:
        """
        Get payment method statistics

        Args:
            start_date: Start date
            end_date: End date

        Returns:
            List of payment method statistics
        """
        payment_stats = (
            Order.objects.filter(
                status="completed", created_at__date__range=[start_date, end_date]
            )
            .values("payment_method")
            .annotate(total_sales=Sum("total"), order_count=Count("id"))
            .order_by("-total_sales")
        )

        # Calculate total for percentages
        total_sales = sum(stat["total_sales"] for stat in payment_stats)

        # Add display names and percentages
        payment_methods = dict(Order.PAYMENT_METHODS)
        for stat in payment_stats:
            stat["payment_method_display"] = payment_methods.get(
                stat["payment_method"], stat["payment_method"]
            )
            stat["percentage"] = (
                (stat["total_sales"] / total_sales * 100) if total_sales > 0 else 0
            )

        return list(payment_stats)

    @staticmethod
    def get_hourly_sales_pattern(date_obj: date) -> List[Dict]:
        """
        Get hourly sales pattern for a specific date

        Args:
            date_obj: Date to analyze

        Returns:
            List of hourly sales data
        """
        hourly_data = []

        for hour in range(24):
            orders = Order.objects.filter(
                status="completed", created_at__date=date_obj, created_at__hour=hour
            )

            stats = orders.aggregate(
                sales=Sum("total") or Decimal("0"),
                orders=Count("id"),
                items=Sum("items__quantity") or 0,
            )

            hourly_data.append(
                {
                    "hour": hour,
                    "hour_display": f"{hour:02d}:00",
                    "sales": stats["sales"],
                    "orders": stats["orders"],
                    "items_sold": stats["items"],
                }
            )

        return hourly_data
