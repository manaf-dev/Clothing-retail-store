from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""

    list_display = ("name", "description", "product_count", "created_at")
    search_fields = ("name", "description")
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")

    def product_count(self, obj):
        """Return the number of products in this category."""
        return obj.products.count()

    product_count.short_description = "Products Count"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for Product model."""

    list_display = (
        "name",
        "category",
        "price",
        "sale_price",
        "stock",
        "stock_status",
        "status",
        "created_at",
    )
    list_display_links = ("name",)
    search_fields = ("name", "description", "category__name")
    list_filter = ("status", "category", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Basic Information", {"fields": ("name", "description", "category")}),
        ("Pricing", {"fields": ("price", "sale_price")}),
        ("Inventory", {"fields": ("stock", "min_stock", "status")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def stock_status(self, obj):
        """Return colored stock status."""
        if obj.stock > 10:
            color = "green"
            status = "In Stock"
        elif obj.stock > 0:
            color = "orange"
            status = "Low Stock"
        else:
            color = "red"
            status = "Out of Stock"

        return format_html('<span style="color: {};">{}</span>', color, status)

    stock_status.short_description = "Stock Status"

    def save_model(self, request, obj, form, change):
        """Custom save logic if needed."""
        super().save_model(request, obj, form, change)
