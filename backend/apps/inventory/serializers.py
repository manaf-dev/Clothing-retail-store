from rest_framework import serializers
from .models import Inventory, Supplier, RestockHistory
from apps.products.serializers import ProductSerializer


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class RestockHistorySerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(read_only=True)

    class Meta:
        model = RestockHistory
        fields = "__all__"


class InventorySerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(read_only=True)
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(),
        source="supplier",
        write_only=True,
        required=False,
    )

    # Product details for frontend compatibility
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_id = serializers.UUIDField(source="product.id", read_only=True)
    sku = serializers.CharField(source="product.sku", read_only=True)
    category_name = serializers.CharField(
        source="product.category.name", read_only=True
    )
    price = serializers.DecimalField(
        source="product.price", max_digits=10, decimal_places=2, read_only=True
    )
    effective_price = serializers.DecimalField(
        source="product.effective_price",
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    # Stock quantity aliased for consistency
    stock_quantity = serializers.IntegerField(source="stock", read_only=True)

    # Size and color (if available in product model, otherwise default)
    size = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()

    # Stock status
    stock_status = serializers.SerializerMethodField()

    class Meta:
        model = Inventory
        fields = [
            "id",
            "product",
            "product_id",
            "product_name",
            "sku",
            "category_name",
            "price",
            "effective_price",
            "stock",
            "stock_quantity",
            "min_stock",
            "size",
            "color",
            "supplier",
            "supplier_id",
            "stock_status",
            "status",
            "created_at",
            "updated_at",
        ]

    def get_size(self, obj):
        """Get product size if available, otherwise return default"""
        return getattr(obj.product, "size", "One Size")

    def get_color(self, obj):
        """Get product color if available, otherwise return default"""
        return getattr(obj.product, "color", "Default")

    def get_stock_status(self, obj):
        """Return human-readable stock status"""
        if obj.stock == 0:
            return "Out of Stock"
        elif obj.stock <= obj.min_stock:
            return "Low Stock"
        return "In Stock"
