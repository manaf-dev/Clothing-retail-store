from typing import Tuple, Dict, Any, Optional
from django.core.paginator import Paginator
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


def create_product(
    data: dict, request=None
) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    Create a new product with the provided data.

    Args:
        data (dict): The product data to create.

    Returns:
        Tuple[Product data | None, error | None]: The created product data or error.
    """
    serializer = ProductSerializer(data=data, context={"request": request})
    if serializer.is_valid():
        product = serializer.save()
        return serializer.data, None
    return None, serializer.errors


def update_product(
    product_id: str, data: dict, request=None
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Update an existing product with the provided data.

    Args:
        product_id (str): The UUID of the product to update.
        data (dict): The updated product data.

    Returns:
        Tuple[Product data | None, error | None]: The updated product data or error.
    """
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return None, "Product not found"

    serializer = ProductSerializer(
        product, data=data, partial=True, context={"request": request}
    )
    if serializer.is_valid():
        updated_product = serializer.save()
        return (
            ProductSerializer(updated_product, context={"request": request}).data,
            None,
        )
    return None, serializer.errors


def delete_product(product_id: str) -> Tuple[bool, Optional[str]]:
    """
    Delete a product by its ID.

    Args:
        product_id (str): The UUID of the product to delete.

    Returns:
        Tuple[bool, error | None]: True if deletion was successful, error otherwise.
    """
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        return True, None
    except Product.DoesNotExist:
        return False, "Product not found"


def get_product_by_id(
    product_id: str,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Retrieve a product by its ID.

    Args:
        product_id (str): The UUID of the product.

    Returns:
        Tuple[Product data | None, error | None]: The product data or error.
    """
    try:
        product = Product.objects.select_related("category").get(id=product_id)
        return ProductSerializer(product).data, None
    except Product.DoesNotExist:
        return None, "Product not found"


def bulk_update_stock(updates: list) -> Tuple[bool, Optional[str]]:
    """
    Bulk update product stock levels.

    Args:
        updates (list): List of dicts with 'id' and 'stock' keys.

    Returns:
        Tuple[bool, error | None]: Success status and error if any.
    """
    try:
        for update in updates:
            Product.objects.filter(id=update["id"]).update(stock=update["stock"])
        return True, None
    except Exception as e:
        return False, str(e)
