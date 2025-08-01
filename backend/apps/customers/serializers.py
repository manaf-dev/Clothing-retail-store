from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "status",
            "is_vip",
            "total_spent",
            "created_at",
            "updated_at",
        ]
