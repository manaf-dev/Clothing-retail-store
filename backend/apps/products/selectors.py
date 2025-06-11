from django.http import HttpRequest
from django.db.models import Q, QuerySet
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


def get_all_products() -> QuerySet[Product]:
    """
    Retrieve all products in the database.

    Returns:
        QuerySet[Product]: A queryset of all products.
    """
    return Product.objects.select_related("category").all()


def get_filtered_products(
    search: str = None,
    category: str = None,
    stock_status: str = None,
    min_price: float = None,
    max_price: float = None,
    ordering: str = None,
) -> QuerySet[Product]:
    """
    Retrieve products with filtering and search capabilities.

    Args:
        search (str): Search term for product name, description
        category (str): Category UUID to filter by
        stock_status (str): Filter by stock status (in_stock, low_stock, out_of_stock)
        min_price (float): Minimum price filter
        max_price (float): Maximum price filter
        ordering (str): Field to order by (e.g., 'name', '-created_at')

    Returns:
        QuerySet[Product]: Filtered queryset of products.
    """
    queryset = Product.objects.select_related("category").all()

    # Search filter
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search)
            | Q(description__icontains=search)
            | Q(category__name__icontains=search)
        )

    # Category filter
    if category:
        queryset = queryset.filter(category_id=category)

    # Stock status filter
    if stock_status:
        if stock_status == "in_stock":
            queryset = queryset.filter(stock__gt=10)
        elif stock_status == "low_stock":
            queryset = queryset.filter(stock__gt=0, stock__lte=10)
        elif stock_status == "out_of_stock":
            queryset = queryset.filter(stock=0)

    # Price range filters
    if min_price is not None:
        queryset = queryset.filter(price__gte=min_price)
    if max_price is not None:
        queryset = queryset.filter(price__lte=max_price)

    # Ordering
    if ordering:
        queryset = queryset.order_by(ordering)
    else:
        queryset = queryset.order_by("name", "created_at")

    return queryset


def get_product_by_id(product_id: str) -> Product | None:
    """
    Retrieve a product by its ID.

    Args:
        product_id (str): The UUID of the product.

    Returns:
        Product | None: The product if found, otherwise None.
    """
    try:
        return Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return None


def get_products_by_category(category_id: str) -> list[Product] | None:
    """
    Retrieve all products in a specific category.

    Args:
        category_id (str): The
            UUID of the category.
    Returns:
        list[Product]: A list of products in the specified category.
    """
    try:
        category = Category.objects.get(id=category_id)
        return list(category.products.all()), None
    except Category.DoesNotExist:
        return None, "Category not found"


def product_representation(
    request: HttpRequest, product: Product, many: bool = False
) -> dict | list[dict]:
    """
    Serialize a product or a list of products for representation.

    Args:
        request (HttpRequest): The HTTP request object.
        product (Product | list[Product]): The product or list of products to serialize.
        many (bool): Whether the product is a single instance or a list.

    Returns:
        dict: Serialized data of the product(s).
    """
    serializer = ProductSerializer(product, many=many, context={"request": request})
    return serializer.data
