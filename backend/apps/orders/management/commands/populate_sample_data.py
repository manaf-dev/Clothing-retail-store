from django.core.management.base import BaseCommand
from apps.customers.models import Customer
from apps.categories.models import Category
from apps.products.models import Product
from apps.orders.models import Order, OrderItem
from decimal import Decimal
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Populate database with sample data for testing"

    def handle(self, *args, **options):
        self.stdout.write("Creating sample data...")

        # Create categories
        categories_data = [
            {"name": "Men's Clothing", "description": "Clothing for men"},
            {"name": "Women's Clothing", "description": "Clothing for women"},
            {"name": "Kids' Clothing", "description": "Clothing for children"},
            {"name": "Accessories", "description": "Fashion accessories"},
            {"name": "Footwear", "description": "Shoes and sandals"},
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data["name"], defaults={"description": cat_data["description"]}
            )
            categories.append(category)
            if created:
                self.stdout.write(f"Created category: {category.name}")

        # Create customers
        customers_data = [
            {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1-555-123-4567",
                "address": "123 Main St, Anytown, USA",
            },
            {
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "phone": "+1-555-987-6543",
                "address": "456 Oak Ave, Sometown, USA",
            },
            {
                "name": "Robert Johnson",
                "email": "robert.j@example.com",
                "phone": "+1-555-765-4321",
                "address": "789 Pine St, Othertown, USA",
            },
            {
                "name": "Sarah Williams",
                "email": "sarah.w@example.com",
                "phone": "+1-555-456-7890",
                "address": "321 Elm St, Newtown, USA",
            },
            {
                "name": "Michael Brown",
                "email": "michael.b@example.com",
                "phone": "+1-555-654-3210",
                "address": "654 Maple Dr, Oldtown, USA",
            },
        ]

        customers = []
        for cust_data in customers_data:
            customer, created = Customer.objects.get_or_create(
                email=cust_data["email"], defaults=cust_data
            )
            customers.append(customer)
            if created:
                self.stdout.write(f"Created customer: {customer.name}")

        # Create products
        products_data = [
            {
                "name": "Classic T-Shirt",
                "description": "Comfortable cotton t-shirt",
                "price": Decimal("29.99"),
                "sale_price": Decimal("24.99"),
                "stock": 50,
                "min_stock": 10,
                "category": categories[0],  # Men's Clothing
                "status": "active",
            },
            {
                "name": "Polo Shirt",
                "description": "Premium polo shirt",
                "price": Decimal("49.99"),
                "stock": 35,
                "min_stock": 8,
                "category": categories[0],  # Men's Clothing
                "status": "active",
            },
            {
                "name": "Denim Jeans",
                "description": "Classic blue denim jeans",
                "price": Decimal("79.99"),
                "stock": 25,
                "min_stock": 5,
                "category": categories[0],  # Men's Clothing
                "status": "active",
            },
            {
                "name": "Summer Dress",
                "description": "Light and airy summer dress",
                "price": Decimal("89.99"),
                "sale_price": Decimal("69.99"),
                "stock": 20,
                "min_stock": 5,
                "category": categories[1],  # Women's Clothing
                "status": "active",
            },
            {
                "name": "Casual Jacket",
                "description": "Versatile casual jacket",
                "price": Decimal("129.99"),
                "stock": 15,
                "min_stock": 3,
                "category": categories[0],  # Men's Clothing
                "status": "active",
            },
            {
                "name": "Kids T-Shirt",
                "description": "Colorful t-shirt for kids",
                "price": Decimal("19.99"),
                "stock": 40,
                "min_stock": 10,
                "category": categories[2],  # Kids' Clothing
                "status": "active",
            },
            {
                "name": "Leather Belt",
                "description": "Genuine leather belt",
                "price": Decimal("34.99"),
                "stock": 30,
                "min_stock": 8,
                "category": categories[3],  # Accessories
                "status": "active",
            },
            {
                "name": "Running Shoes",
                "description": "Comfortable running shoes",
                "price": Decimal("99.99"),
                "sale_price": Decimal("79.99"),
                "stock": 18,
                "min_stock": 5,
                "category": categories[4],  # Footwear
                "status": "active",
            },
        ]

        products = []
        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                name=prod_data["name"], defaults=prod_data
            )
            products.append(product)
            if created:
                self.stdout.write(f"Created product: {product.name}")

        # Create sample orders
        payment_methods = ["cash", "card", "mobile_money", "bank_transfer"]
        statuses = ["completed", "pending", "processing"]

        for i in range(15):
            # Random date within last 30 days
            days_ago = random.randint(0, 30)
            order_date = datetime.now() - timedelta(days=days_ago)

            # Random customer (some orders without customer for walk-ins)
            customer = random.choice(customers) if random.random() > 0.3 else None

            order = Order.objects.create(
                customer=customer,
                payment_method=random.choice(payment_methods),
                status=random.choice(statuses),
                notes=f"Sample order {i+1}",
                served_by="Admin",
                created_at=order_date,
            )

            # Add 1-4 random items to each order
            num_items = random.randint(1, 4)
            subtotal = Decimal("0")

            for _ in range(num_items):
                product = random.choice(products)
                quantity = random.randint(1, 3)
                price = product.sale_price if product.sale_price else product.price

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    quantity=quantity,
                    price=price,
                )

                subtotal += price * quantity

            # Update order totals
            order.subtotal = subtotal
            order.tax_amount = subtotal * Decimal("0.085")  # 8.5% tax
            order.total = order.subtotal + order.tax_amount
            order.save()

            self.stdout.write(f"Created order: {order.order_number}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created sample data:\n"
                f"- {len(categories)} categories\n"
                f"- {len(customers)} customers\n"
                f"- {len(products)} products\n"
                f"- 15 sample orders"
            )
        )
