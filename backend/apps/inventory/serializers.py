from rest_framework import serializers
from .models import Inventory, Supplier, RestockHistory


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class RestockHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RestockHistory
        fields = "__all__"


class InventorySerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(read_only=True)
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(), source="supplier", write_only=True
    )

    class Meta:
        model = Inventory
        fields = [
            "id",
            "product",
            "stock",
            "min_stock",
            "supplier",
            "supplier_id",
            "restock_history",
            "status",
            "created_at",
            "updated_at",
        ]
