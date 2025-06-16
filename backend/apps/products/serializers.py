from rest_framework import serializers
from decimal import Decimal
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""

    class Meta:
        model = Category
        fields = ["id", "name", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def to_representation(self, instance):
        """Customize the output representation."""
        data = super().to_representation(instance)
        return data


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for product list views."""

    category = CategorySerializer(read_only=True)
    stock_status = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "image",
            "category",
            "price",
            "sale_price",
            "stock",
            "stock_status",
            "status",
            "created_at",
        ]

    def get_stock_status(self, obj):
        """Return human-readable stock status."""
        if obj.stock > 10:
            return "In Stock"
        elif obj.stock > 0:
            return "Low Stock"
        return "Out of Stock"


class ProductSerializer(serializers.ModelSerializer):
    """Main serializer for Product model with full details."""
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
        allow_null=False,
    )
    stock_status = serializers.SerializerMethodField()
    is_on_sale = serializers.SerializerMethodField()
    effective_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "image",
            "price",
            "sale_price",
            "stock",
            "min_stock",
            "category",
            "category_id",
            "status",
            "stock_status",
            "is_on_sale",
            "effective_price",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_stock_status(self, obj):
        """Return human-readable stock status."""
        if obj.stock > 10:
            return "In Stock"
        elif obj.stock > 0:
            return "Low Stock"
        return "Out of Stock"

    def get_is_on_sale(self, obj):
        """Check if product is on sale."""
        return obj.sale_price is not None and obj.sale_price > 0

    def get_effective_price(self, obj):
        """Return the effective selling price (sale price if available, otherwise regular price)."""
        if obj.sale_price and obj.sale_price > 0:
            return obj.sale_price
        return obj.price

    def validate(self, attrs):
        """Validate product data."""
        price = attrs.get("price")
        sale_price = attrs.get("sale_price")
        stock = attrs.get("stock")
        min_stock = attrs.get("min_stock")

        # Validate stock
        if stock is not None and stock < 0:
            raise serializers.ValidationError({"stock": "Stock cannot be negative."})

        # Validate minimum stock
        if min_stock is not None and min_stock < 0:
            raise serializers.ValidationError(
                {"min_stock": "Minimum stock cannot be negative."}
            )

        # Validate price
        if price is not None and price <= 0:
            raise serializers.ValidationError(
                {"price": "Price must be greater than zero."}
            )

        return attrs

    def create(self, validated_data):
        """Create a new product."""
        category_data = validated_data.pop("category", None)
        if category_data:
            validated_data["category"] = category_data
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update an existing product."""
        category_data = validated_data.pop("category", None)
        if category_data:
            instance.category = category_data
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """Customize the output representation."""
        data = super().to_representation(instance)

        # Format prices to 2 decimal places
        if data.get("price"):
            data["price"] = f"{float(data['price']):.2f}"
        if data.get("sale_price"):
            data["sale_price"] = f"{float(data['sale_price']):.2f}"
        if data.get("effective_price"):
            data["effective_price"] = f"{float(data['effective_price']):.2f}"
        # build absolute URL for image with protocol and domain
        if data.get("image"):
            request = self.context.get("request")
            if request:
                data["image"] = request.build_absolute_uri(data["image"])

        return data


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating products."""

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "sale_price",
            "stock",
            "min_stock",
            "category_id",
            "status",
        ]

    def validate(self, attrs):
        """Validate product data."""
        return ProductSerializer().validate(attrs)
