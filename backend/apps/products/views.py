from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .selectors import get_filtered_products
from .services import (
    create_product,
    update_product,
    delete_product,
    get_product_by_id,
    bulk_update_stock,
)


class ProductViewSet(viewsets.ViewSet):
    """
    ViewSet for handling product operations.
    Provides CRUD operations and filtering capabilities.
    """

    def list(self, request: Request) -> Response:
        """
        List all products with filtering, searching, and pagination.

        Query Parameters:
        - search: Search term for product name/description
        - category: Category UUID
        - stock_status: in_stock, low_stock, out_of_stock
        - min_price: Minimum price
        - max_price: Maximum price
        - ordering: Field to order by
        - page: Page number
        - page_size: Items per page (default: 10)
        """
        # Get query parameters
        search = request.query_params.get("search", None)
        category = request.query_params.get("category", None)
        stock_status = request.query_params.get("stock_status", None)
        min_price = request.query_params.get("min_price", None)
        max_price = request.query_params.get("max_price", None)
        ordering = request.query_params.get("ordering", None)
        page = request.query_params.get("page", 1)
        page_size = int(request.query_params.get("page_size", 10))

        # Convert price parameters to float if provided
        try:
            min_price = float(min_price) if min_price else None
            max_price = float(max_price) if max_price else None
        except (ValueError, TypeError):
            min_price = max_price = None

        # Get filtered products
        products = get_filtered_products(
            search=search,
            category=category,
            stock_status=stock_status,
            min_price=min_price,
            max_price=max_price,
            ordering=ordering,
        )

        # Pagination
        paginator = Paginator(products, page_size)
        try:
            products_page = paginator.page(page)
        except PageNotAnInteger:
            products_page = paginator.page(1)
        except EmptyPage:
            products_page = paginator.page(paginator.num_pages)

        # Serialize data
        serializer = ProductSerializer(
            products_page, many=True, context={"request": request}
        )

        return Response(
            {
                "results": serializer.data,
                "count": paginator.count,
                "num_pages": paginator.num_pages,
                "current_page": products_page.number,
                "has_next": products_page.has_next(),
                "has_previous": products_page.has_previous(),
            },
            status=status.HTTP_200_OK,
        )

    def create(self, request: Request) -> Response:
        """Create a new product."""
        data = request.data
        product_data, error = create_product(data, request=request)

        if error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        return Response(product_data, status=status.HTTP_201_CREATED)

    def retrieve(self, request: Request, pk=None) -> Response:
        """Retrieve a specific product by ID."""
        product_data, error = get_product_by_id(pk)

        if error:
            return Response({"error": error}, status=status.HTTP_404_NOT_FOUND)

        return Response(product_data, status=status.HTTP_200_OK)

    def update(self, request: Request, pk=None) -> Response:
        """Update a specific product."""
        data = request.data
        product_data, error = update_product(pk, data, request=request)

        if error:
            if error == "Product not found":
                return Response({"error": error}, status=status.HTTP_404_NOT_FOUND)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        return Response(product_data, status=status.HTTP_200_OK)

    def partial_update(self, request: Request, pk=None) -> Response:
        """Partially update a specific product."""
        return self.update(request, pk)

    def destroy(self, request: Request, pk=None) -> Response:
        """Delete a specific product."""
        success, error = delete_product(pk)

        if not success:
            return Response({"error": error}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {"message": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(detail=False, methods=["get"])
    def low_stock(self, request: Request) -> Response:
        """Get products with low stock levels."""
        products = Product.objects.filter(stock__lte=10, stock__gt=0).select_related(
            "category"
        )
        serializer = ProductSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def out_of_stock(self, request: Request) -> Response:
        """Get products that are out of stock."""
        products = Product.objects.filter(stock=0).select_related("category")
        serializer = ProductSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def bulk_update_stock(self, request: Request) -> Response:
        """Bulk update stock levels for multiple products."""
        updates = request.data.get("updates", [])

        if not updates:
            return Response(
                {"error": "No updates provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        success, error = bulk_update_stock(updates)

        if not success:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "Stock levels updated successfully"}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["get"])
    def search(self, request: Request) -> Response:
        """Advanced search endpoint for products."""
        query = request.query_params.get("q", "")

        if not query:
            return Response({"results": []}, status=status.HTTP_200_OK)

        products = get_filtered_products(search=query)[:20]  # Limit to 20 results
        serializer = ProductSerializer(
            products, many=True, context={"request": request}
        )

        return Response({"results": serializer.data}, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling category operations.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request: Request) -> Response:
        """List all categories."""
        categories = Category.objects.all().order_by("name")
        serializer = CategorySerializer(
            categories, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def products(self, request: Request, pk=None) -> Response:
        """Get all products in a specific category."""
        try:
            category = Category.objects.get(pk=pk)
            products = category.products.all().order_by("name")
            serializer = ProductSerializer(
                products, many=True, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND
            )
