from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline admin for order items"""

    model = OrderItem
    extra = 0
    readonly_fields = ("line_total",)
    fields = ("product", "product_name", "quantity", "price", "discount", "line_total")

    def line_total(self, obj):
        if obj.id:
            return f"₵{obj.line_total:.2f}"
        return "-"

    line_total.short_description = "Line Total"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Order model"""

    list_display = [
        "order_number",
        # "customer_link",
        "total_formatted",
        "status_badge",
        "payment_status_badge",
        "payment_method",
        "item_count_display",
        "served_by",
        "created_at_formatted",
    ]
    list_filter = [
        "status",
        "payment_status",
        "payment_method",
        "created_at",
        "served_by",
    ]
    search_fields = [
        "order_number",
        "customer_name",
        "served_by",
        "notes",
    ]
    readonly_fields = [
        "id",
        "order_number",
        "subtotal",
        "total",
        "item_count",
        "total_quantity",
        "created_at",
        "updated_at",
    ]
    inlines = [OrderItemInline]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    fieldsets = (
        (
            "Order Information",
            {
                "fields": (
                    "id",
                    "order_number",
                    "status",
                    "created_at",
                    "updated_at",
                    "completed_at",
                )
            },
        ),
        # ("Customer", {"fields": ("customer",)}),
        ("Payment", {"fields": ("payment_method", "payment_status")}),
        ("Amounts", {"fields": ("subtotal", "tax_amount", "discount_amount", "total")}),
        (
            "Order Details",
            {"fields": ("item_count", "total_quantity", "served_by", "notes")},
        ),
    )

    # def customer_link(self, obj):
    #     """Display customer name as a link to customer admin"""
    #     if obj.customer:
    #         url = reverse("admin:customers_customer_change", args=[obj.customer.id])
    #         return format_html('<a href="{}">{}</a>', url, obj.customer.name)
    #     return "Walk-in Customer"

    # customer_link.short_description = "Customer"

    def total_formatted(self, obj):
        """Format total amount with currency"""
        return f"₵{obj.total:.2f}"

    total_formatted.short_description = "Total"
    total_formatted.admin_order_field = "total"

    def status_badge(self, obj):
        """Display status as a colored badge"""
        colors = {
            "pending": "#fbbf24",  # yellow
            "processing": "#3b82f6",  # blue
            "completed": "#10b981",  # green
            "cancelled": "#ef4444",  # red
            "refunded": "#8b5cf6",  # purple
        }
        color = colors.get(obj.status, "#6b7280")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; '
            'border-radius: 4px; font-size: 12px;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_badge.short_description = "Status"

    def payment_status_badge(self, obj):
        """Display payment status as a colored badge"""
        colors = {
            "pending": "#fbbf24",  # yellow
            "paid": "#10b981",  # green
            "partially_paid": "#f59e0b",  # orange
            "failed": "#ef4444",  # red
            "refunded": "#8b5cf6",  # purple
        }
        color = colors.get(obj.payment_status, "#6b7280")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; '
            'border-radius: 4px; font-size: 12px;">{}</span>',
            color,
            obj.get_payment_status_display(),
        )

    payment_status_badge.short_description = "Payment Status"

    def item_count_display(self, obj):
        """Display item count"""
        return f"{obj.item_count} items"

    item_count_display.short_description = "Items"

    def created_at_formatted(self, obj):
        """Format created_at timestamp"""
        local_time = timezone.localtime(obj.created_at)
        return local_time.strftime("%Y-%m-%d %H:%M")

    created_at_formatted.short_description = "Created"
    created_at_formatted.admin_order_field = "created_at"

    # def get_queryset(self, request):
    #     """Optimize queryset with select_related"""
    #     return super().get_queryset(request).select_related("customer")

    actions = ["mark_as_completed", "mark_as_cancelled", "mark_as_paid"]

    def mark_as_completed(self, request, queryset):
        """Mark selected orders as completed"""
        updated = queryset.filter(status__in=["pending", "processing"]).update(
            status="completed", completed_at=timezone.now()
        )
        self.message_user(request, f"{updated} orders marked as completed.")

    mark_as_completed.short_description = "Mark selected orders as completed"

    def mark_as_cancelled(self, request, queryset):
        """Mark selected orders as cancelled"""
        updated = queryset.filter(status__in=["pending", "processing"]).update(
            status="cancelled"
        )
        self.message_user(request, f"{updated} orders marked as cancelled.")

    mark_as_cancelled.short_description = "Mark selected orders as cancelled"

    def mark_as_paid(self, request, queryset):
        """Mark selected orders as paid"""
        updated = queryset.update(payment_status="paid")
        self.message_user(request, f"{updated} orders marked as paid.")

    mark_as_paid.short_description = "Mark selected orders as paid"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin interface for OrderItem model"""

    list_display = [
        "order_link",
        "product_link",
        "product_name",
        "quantity",
        "price_formatted",
        "discount_formatted",
        "line_total_formatted",
        "order_status",
    ]
    list_filter = ["order__status", "order__created_at", "product__category"]
    search_fields = [
        "product_name",
        "product__name",
        "order__order_number",
        # "order__customer__name",
    ]
    readonly_fields = ["id", "line_total"]
    ordering = ["-order__created_at"]

    def order_link(self, obj):
        """Display order number as a link"""
        url = reverse("admin:orders_order_change", args=[obj.order.id])
        return format_html('<a href="{}">{}</a>', url, obj.order.order_number)

    order_link.short_description = "Order"

    def product_link(self, obj):
        """Display product name as a link"""
        if obj.product:
            url = reverse("admin:products_product_change", args=[obj.product.id])
            return format_html('<a href="{}">{}</a>', url, obj.product.name)
        return obj.product_name

    product_link.short_description = "Product"

    def price_formatted(self, obj):
        """Format price with currency"""
        return f"₵{obj.price:.2f}"

    price_formatted.short_description = "Price"
    price_formatted.admin_order_field = "price"

    def discount_formatted(self, obj):
        """Format discount with currency"""
        return f"₵{obj.discount:.2f}" if obj.discount else "-"

    discount_formatted.short_description = "Discount"

    def line_total_formatted(self, obj):
        """Format line total with currency"""
        return f"₵{obj.line_total:.2f}"

    line_total_formatted.short_description = "Line Total"

    def order_status(self, obj):
        """Display order status"""
        return obj.order.get_status_display()

    order_status.short_description = "Order Status"

    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return (
            super()
            .get_queryset(request)
            .select_related("order", "product", "product__category")
        )


# Admin site customization
admin.site.site_header = "Clothing Retail Store Admin"
admin.site.site_title = "CRS Admin"
admin.site.index_title = "Welcome to Clothing Retail Store Administration"
