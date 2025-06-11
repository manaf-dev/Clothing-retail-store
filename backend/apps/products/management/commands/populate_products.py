"""
Management command to populate the database with sample products and categories.
Usage: python manage.py populate_products
"""

from django.core.management.base import BaseCommand
from decimal import Decimal
from apps.products.models import Category, Product


class Command(BaseCommand):
    help = "Populate database with sample products and categories"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before populating",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Clearing existing data...")
            Product.objects.all().delete()
            Category.objects.all().delete()

        # Create categories
        categories_data = [
            {
                "name": "Men's Clothing",
                "description": "Clothing items for men including shirts, pants, and accessories",
            },
            {
                "name": "Women's Clothing",
                "description": "Fashionable clothing for women including dresses, tops, and more",
            },
            {
                "name": "Kids' Clothing",
                "description": "Comfortable and stylish clothing for children",
            },
            {
                "name": "Accessories",
                "description": "Fashion accessories including bags, jewelry, and belts",
            },
            {"name": "Footwear", "description": "Shoes and footwear for all occasions"},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data["name"], defaults={"description": cat_data["description"]}
            )
            categories[cat_data["name"]] = category
            if created:
                self.stdout.write(f"Created category: {category.name}")

        # Create sample products
        products_data = [
            {
                "name": "Men's Classic Jeans",
                "description": "Comfortable blue denim jeans with a classic fit",
                "price": Decimal("59.99"),
                "sale_price": None,
                "stock": 45,
                "min_stock": 5,
                "category": categories["Men's Clothing"],
            },
            {
                "name": "Women's Summer Dress",
                "description": "Light and breezy summer dress with floral pattern",
                "price": Decimal("79.99"),
                "sale_price": Decimal("59.99"),
                "stock": 23,
                "min_stock": 3,
                "category": categories["Women's Clothing"],
            },
            {
                "name": "Kids' T-Shirt Pack",
                "description": "Pack of 3 colorful t-shirts for children",
                "price": Decimal("24.99"),
                "sale_price": None,
                "stock": 67,
                "min_stock": 10,
                "category": categories["Kids' Clothing"],
            },
            {
                "name": "Leather Handbag",
                "description": "Elegant leather handbag with multiple compartments",
                "price": Decimal("129.99"),
                "sale_price": Decimal("99.99"),
                "stock": 12,
                "min_stock": 2,
                "category": categories["Accessories"],
            },
            {
                "name": "Running Shoes",
                "description": "Lightweight running shoes with excellent cushioning",
                "price": Decimal("89.99"),
                "sale_price": None,
                "stock": 8,
                "min_stock": 3,
                "category": categories["Footwear"],
            },
            {
                "name": "Men's Formal Shirt",
                "description": "Crisp white formal shirt perfect for business occasions",
                "price": Decimal("49.99"),
                "sale_price": None,
                "stock": 34,
                "min_stock": 5,
                "category": categories["Men's Clothing"],
            },
            {
                "name": "Women's Leather Jacket",
                "description": "Stylish black leather jacket with modern design",
                "price": Decimal("199.99"),
                "sale_price": Decimal("159.99"),
                "stock": 6,
                "min_stock": 2,
                "category": categories["Women's Clothing"],
            },
            {
                "name": "Kids' Winter Coat",
                "description": "Warm winter coat with hood for children",
                "price": Decimal("69.99"),
                "sale_price": None,
                "stock": 15,
                "min_stock": 3,
                "category": categories["Kids' Clothing"],
            },
            {
                "name": "Silver Watch",
                "description": "Elegant silver watch with sapphire crystal",
                "price": Decimal("249.99"),
                "sale_price": None,
                "stock": 4,
                "min_stock": 1,
                "category": categories["Accessories"],
            },
            {
                "name": "Sneakers",
                "description": "Casual sneakers perfect for everyday wear",
                "price": Decimal("79.99"),
                "sale_price": Decimal("69.99"),
                "stock": 28,
                "min_stock": 5,
                "category": categories["Footwear"],
            },
            {
                "name": "Business Suit",
                "description": "Professional two-piece business suit",
                "price": Decimal("299.99"),
                "sale_price": None,
                "stock": 9,
                "min_stock": 2,
                "category": categories["Men's Clothing"],
            },
            {
                "name": "Evening Gown",
                "description": "Elegant evening gown for special occasions",
                "price": Decimal("189.99"),
                "sale_price": None,
                "stock": 3,
                "min_stock": 1,
                "category": categories["Women's Clothing"],
            },
            {
                "name": "Low Stock Item",
                "description": "This item has very low stock for testing",
                "price": Decimal("19.99"),
                "sale_price": None,
                "stock": 2,
                "min_stock": 5,
                "category": categories["Accessories"],
            },
            {
                "name": "Out of Stock Item",
                "description": "This item is out of stock for testing",
                "price": Decimal("29.99"),
                "sale_price": None,
                "stock": 0,
                "min_stock": 3,
                "category": categories["Accessories"],
            },
        ]

        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data["name"], defaults=product_data
            )
            if created:
                self.stdout.write(f"Created product: {product.name}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully populated database with {Category.objects.count()} categories "
                f"and {Product.objects.count()} products"
            )
        )
