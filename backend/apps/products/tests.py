"""
Comprehensive test suite for the Products app.
Tests API endpoints, models, serializers, and business logic.
"""

from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class CategoryModelTest(TestCase):
    """Test cases for Category model."""

    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(
            name="Test Category", description="Test category description"
        )

    def test_category_creation(self):
        """Test category creation."""
        self.assertEqual(self.category.name, "Test Category")
        self.assertEqual(str(self.category), "Test Category")

    def test_category_str_representation(self):
        """Test category string representation."""
        self.assertEqual(str(self.category), "Test Category")


class ProductModelTest(TestCase):
    """Test cases for Product model."""

    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(
            name="Electronics", description="Electronic products"
        )
        self.product = Product.objects.create(
            name="Test Product",
            description="Test product description",
            price=Decimal("99.99"),
            stock=50,
            min_stock=5,
            category=self.category,
        )

    def test_product_creation(self):
        """Test product creation."""
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.price, Decimal("99.99"))
        self.assertEqual(self.product.stock, 50)
        self.assertEqual(self.product.category, self.category)

    def test_product_str_representation(self):
        """Test product string representation."""
        self.assertEqual(str(self.product), "Test Product")

    def test_product_with_sale_price(self):
        """Test product with sale price."""
        self.product.sale_price = Decimal("79.99")
        self.product.save()
        self.assertEqual(self.product.sale_price, Decimal("79.99"))


class CategorySerializerTest(TestCase):
    """Test cases for CategorySerializer."""

    def setUp(self):
        """Set up test data."""
        self.category_data = {
            "name": "Fashion",
            "description": "Fashion and clothing items",
        }
        self.category = Category.objects.create(**self.category_data)

    def test_category_serialization(self):
        """Test category serialization."""
        serializer = CategorySerializer(self.category)
        data = serializer.data
        self.assertEqual(data["name"], self.category_data["name"])
        self.assertEqual(data["description"], self.category_data["description"])

    def test_category_deserialization(self):
        """Test category deserialization."""
        serializer = CategorySerializer(data=self.category_data)
        self.assertTrue(serializer.is_valid())


class ProductSerializerTest(TestCase):
    """Test cases for ProductSerializer."""

    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(
            name="Books", description="Books and literature"
        )
        self.product_data = {
            "name": "Django Book",
            "description": "Learn Django framework",
            "price": "49.99",
            "stock": 100,
            "min_stock": 10,
            "category_id": str(self.category.id),
        }
        self.product = Product.objects.create(
            name="Django Book",
            description="Learn Django framework",
            price=Decimal("49.99"),
            stock=100,
            min_stock=10,
            category=self.category,
        )

    def test_product_serialization(self):
        """Test product serialization."""
        serializer = ProductSerializer(self.product)
        data = serializer.data
        self.assertEqual(data["name"], "Django Book")
        self.assertEqual(float(data["price"]), 49.99)
        self.assertEqual(data["stock"], 100)

    def test_product_deserialization(self):
        """Test product deserialization."""
        serializer = ProductSerializer(data=self.product_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_product_validation_sale_price_error(self):
        """Test validation error when sale price >= regular price."""
        invalid_data = self.product_data.copy()
        invalid_data["sale_price"] = "59.99"  # Higher than regular price
        serializer = ProductSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("sale_price", serializer.errors)

    def test_product_validation_negative_stock(self):
        """Test validation error for negative stock."""
        invalid_data = self.product_data.copy()
        invalid_data["stock"] = -5
        serializer = ProductSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("stock", serializer.errors)


class ProductAPITest(APITestCase):
    """Test cases for Product API endpoints."""

    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(
            name="Sports", description="Sports equipment"
        )
        self.product = Product.objects.create(
            name="Basketball",
            description="Professional basketball",
            price=Decimal("29.99"),
            stock=25,
            min_stock=5,
            category=self.category,
        )
        self.product_data = {
            "name": "Football",
            "description": "Professional football",
            "price": "39.99",
            "stock": 30,
            "min_stock": 5,
            "category_id": str(self.category.id),
        }

    def test_get_products_list(self):
        """Test GET /api/products/ endpoint."""
        url = reverse("product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)

    def test_create_product(self):
        """Test POST /api/products/ endpoint."""
        url = reverse("product-list")
        response = self.client.post(url, self.product_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_get_product_detail(self):
        """Test GET /api/products/{id}/ endpoint."""
        url = reverse("product-detail", kwargs={"pk": self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)

    def test_update_product(self):
        """Test PUT /api/products/{id}/ endpoint."""
        url = reverse("product-detail", kwargs={"pk": self.product.id})
        updated_data = self.product_data.copy()
        updated_data["name"] = "Updated Basketball"
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Updated Basketball")

    def test_delete_product(self):
        """Test DELETE /api/products/{id}/ endpoint."""
        url = reverse("product-detail", kwargs={"pk": self.product.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_product_search(self):
        """Test product search functionality."""
        url = reverse("product-search")
        response = self.client.get(url, {"q": "basketball"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_product_filtering_by_category(self):
        """Test product filtering by category."""
        url = reverse("product-list")
        response = self.client.get(url, {"category": str(self.category.id)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_product_filtering_by_stock_status(self):
        """Test product filtering by stock status."""
        url = reverse("product-list")
        response = self.client.get(url, {"stock_status": "in_stock"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_low_stock_endpoint(self):
        """Test low stock products endpoint."""
        # Create a low stock product
        Product.objects.create(
            name="Low Stock Item",
            price=Decimal("19.99"),
            stock=5,  # Low stock
            min_stock=3,
            category=self.category,
        )
        url = reverse("product-low-stock")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_out_of_stock_endpoint(self):
        """Test out of stock products endpoint."""
        # Create an out of stock product
        Product.objects.create(
            name="Out of Stock Item",
            price=Decimal("15.99"),
            stock=0,  # Out of stock
            min_stock=1,
            category=self.category,
        )
        url = reverse("product-out-of-stock")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class CategoryAPITest(APITestCase):
    """Test cases for Category API endpoints."""

    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(
            name="Technology", description="Technology products"
        )
        self.category_data = {
            "name": "Home & Garden",
            "description": "Home and garden products",
        }

    def test_get_categories_list(self):
        """Test GET /api/products/categories/ endpoint."""
        url = reverse("category-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_category(self):
        """Test POST /api/products/categories/ endpoint."""
        url = reverse("category-list")
        response = self.client.post(url, self.category_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_get_category_products(self):
        """Test GET /api/products/categories/{id}/products/ endpoint."""
        # Create a product in the category
        Product.objects.create(
            name="Tech Product",
            price=Decimal("199.99"),
            stock=15,
            min_stock=3,
            category=self.category,
        )
        url = reverse("category-products", kwargs={"pk": self.category.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
