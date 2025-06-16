from django.core.management.base import BaseCommand
from apps.products.models import Product
from apps.inventory.models import Inventory


class Command(BaseCommand):
    help = "Sync product stock with inventory records"

    def handle(self, *args, **options):
        products = Product.objects.all()
        created_count = 0
        updated_count = 0

        for product in products:
            inventory, created = Inventory.objects.get_or_create(
                product=product,
                defaults={
                    "stock": product.stock,
                    "min_stock": product.min_stock or 1,
                    "status": "in_stock" if product.stock > 0 else "out_of_stock",
                },
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created inventory for product: {product.name}")
                )
            else:
                # Update existing inventory to match product stock
                if inventory.stock != product.stock:
                    inventory.stock = product.stock
                    inventory.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"Updated inventory for product: {product.name}"
                        )
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"Sync completed. Created: {created_count}, Updated: {updated_count}"
            )
        )
