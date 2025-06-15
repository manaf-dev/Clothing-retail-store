from django.db import models
from django.db.models import Sum, F
from apps.products.models import Product
import uuid


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("refunded", "Refunded"),
    ]
    PAYMENT_METHODS = [
        ("cash", "Cash"),
        ("card", "Card"),
        ("mobile_money", "Mobile Money"),
        ("bank_transfer", "Bank Transfer"),
        ("credit", "Credit"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    # Removed customer field for in-store management system
    customer_name = models.CharField(
        max_length=100, blank=True, help_text="Optional customer name for receipt"
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("paid", "Paid"),
            ("partially_paid", "Partially Paid"),
            ("failed", "Failed"),
            ("refunded", "Refunded"),
        ],
        default="pending",
    )
    notes = models.TextField(blank=True)
    served_by = models.CharField(max_length=100, blank=True)  # Staff member name
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["payment_status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["order_number"]),
        ]

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number like ORD-20250611-001
            from django.utils import timezone

            today = timezone.now().strftime("%Y%m%d")
            last_order = (
                Order.objects.filter(order_number__startswith=f"ORD-{today}")
                .order_by("-order_number")
                .first()
            )

            if last_order:
                last_num = int(last_order.order_number.split("-")[-1])
                new_num = last_num + 1
            else:
                new_num = 1

            self.order_number = f"ORD-{today}-{new_num:03d}"
        super().save(*args, **kwargs)

    def calculate_totals(self):
        """Calculate subtotal, tax, and total from order items"""
        items_total = (
            self.items.aggregate(total=Sum(F("quantity") * F("price")))["total"] or 0
        )

        self.subtotal = items_total
        # You can add tax calculation logic here
        # self.tax_amount = self.subtotal * Decimal('0.15')  # 15% tax
        self.total = self.subtotal + self.tax_amount - self.discount_amount
        self.save(update_fields=["subtotal", "tax_amount", "total"])

    @property
    def item_count(self):
        return self.items.count()

    @property
    def total_quantity(self):
        return self.items.aggregate(total=Sum("quantity"))["total"] or 0

    def __str__(self):
        return f"Order {self.order_number}"


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(
        max_length=200, default=""
    )  # Store name in case product is deleted
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Price at time of sale
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        indexes = [
            models.Index(fields=["order", "product"]),
        ]

    def save(self, *args, **kwargs):
        if self.product and not self.product_name:
            self.product_name = self.product.name
        super().save(*args, **kwargs)

    @property
    def line_total(self):
        return (self.price * self.quantity) - self.discount

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"
