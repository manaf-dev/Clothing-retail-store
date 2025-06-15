from rest_framework import serializers
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from .models import Order, OrderItem
from apps.products.models import Product


class OrderItemReadSerializer(serializers.ModelSerializer):
    """Serializer for reading order items with product details"""

    product_details = serializers.SerializerMethodField()
    line_total = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "price",
            "discount",
            "line_total",
            "product_details",
        ]

    def get_product_details(self, obj):
        if obj.product:
            return {
                "id": obj.product.id,
                "name": obj.product.name,
                "current_price": str(obj.product.price),
                "current_stock": obj.product.stock,
                "category": obj.product.category.name if obj.product.category else None,
            }
        return None


class OrderItemWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating order items"""

    product_id = serializers.UUIDField(source="product.id")

    class Meta:
        model = OrderItem
        fields = ["product_id", "quantity", "price", "discount"]

    def validate_product_id(self, value):
        try:
            product = Product.objects.get(id=value)
            if product.status != "active":
                raise serializers.ValidationError("Product is not active")
            return value
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist")

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value


class OrderReadSerializer(serializers.ModelSerializer):
    """Serializer for reading orders with all details"""

    items = OrderItemReadSerializer(many=True, read_only=True)
    item_count = serializers.ReadOnlyField()
    total_quantity = serializers.ReadOnlyField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    payment_method_display = serializers.CharField(
        source="get_payment_method_display", read_only=True
    )
    payment_status_display = serializers.CharField(
        source="get_payment_status_display", read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "customer_name",
            "subtotal",
            "tax_amount",
            "discount_amount",
            "total",
            "status",
            "status_display",
            "payment_method",
            "payment_method_display",
            "payment_status",
            "payment_status_display",
            "notes",
            "served_by",
            "created_at",
            "updated_at",
            "completed_at",
            "items",
            "item_count",
            "total_quantity",
        ]


class OrderWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating orders"""

    items = OrderItemWriteSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "customer_name",
            "status",
            "payment_method",
            "payment_status",
            "tax_amount",
            "discount_amount",
            "notes",
            "served_by",
            "items",
        ]

    def validate_items(self, value):
        print("Validating order items:", value)
        if not value:
            raise serializers.ValidationError("Order must contain at least one item")
        return value

    @transaction.atomic
    def create(self, validated_data):
        print("Creating order serializer with data:", validated_data)
        items_data = validated_data.pop("items")

        # Create order
        order = Order.objects.create(**validated_data)

        # Create order items and calculate totals
        subtotal = Decimal("0")
        for item_data in items_data:
            product = Product.objects.get(id=item_data["product"]["id"])

            # Check stock availability
            if product.stock < item_data["quantity"]:
                raise serializers.ValidationError(
                    f"Insufficient stock for {product.name}. Available: {product.stock}"
                )

            # Use current product price if not provided
            if "price" not in item_data:
                item_data["price"] = product.effective_price

            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                quantity=item_data["quantity"],
                price=item_data["price"],
                discount=item_data.get("discount", 0),
            )

            # Update product stock
            product.stock -= item_data["quantity"]
            product.save(update_fields=["stock"])

            subtotal += order_item.line_total

        # Update order totals
        order.subtotal = subtotal
        order.total = order.subtotal + order.tax_amount - order.discount_amount
        order.save(update_fields=["subtotal", "total"])

        return order

    @transaction.atomic
    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", [])

        # Update order fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # If order is being completed, set completed_at
        if instance.status == "completed" and not instance.completed_at:
            instance.completed_at = timezone.now()

        instance.save()

        # Update items if provided
        if items_data:
            # This is a simplified update - in production you might want more sophisticated logic
            instance.items.all().delete()

            subtotal = Decimal("0")
            for item_data in items_data:
                product = Product.objects.get(id=item_data["product"]["id"])

                order_item = OrderItem.objects.create(
                    order=instance,
                    product=product,
                    product_name=product.name,
                    quantity=item_data["quantity"],
                    price=item_data["price"],
                    discount=item_data.get("discount", 0),
                )

                subtotal += order_item.line_total

            # Update order totals
            instance.subtotal = subtotal
            instance.total = (
                instance.subtotal + instance.tax_amount - instance.discount_amount
            )
            instance.save(update_fields=["subtotal", "total"])

        return instance


class SalesReportSerializer(serializers.Serializer):
    """Serializer for sales reports and analytics"""

    date = serializers.DateField()
    total_sales = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_orders = serializers.IntegerField()
    total_items_sold = serializers.IntegerField()
    average_order_value = serializers.DecimalField(max_digits=10, decimal_places=2)


class TopProductSerializer(serializers.Serializer):
    """Serializer for top-selling products"""

    product_id = serializers.UUIDField()
    product_name = serializers.CharField()
    total_quantity = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    order_count = serializers.IntegerField()


class PaymentMethodReportSerializer(serializers.Serializer):
    """Serializer for payment method analytics"""

    payment_method = serializers.CharField()
    payment_method_display = serializers.CharField()
    total_sales = serializers.DecimalField(max_digits=12, decimal_places=2)
    order_count = serializers.IntegerField()
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
