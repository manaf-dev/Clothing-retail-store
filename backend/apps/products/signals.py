from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product


@receiver(post_save, sender=Product)
def create_or_sync_inventory(sender, instance: Product, created, **kwargs):
    """Ensure an Inventory record exists and stays in sync with product stock.

    When a product is created it should appear in inventory automatically.
    Also sync stock/min_stock on subsequent saves.
    """
    try:
        from apps.inventory.models import Inventory

        inventory, inv_created = Inventory.objects.get_or_create(
            product=instance,
            defaults={
                "stock": instance.stock,
                "min_stock": getattr(instance, "min_stock", 1) or 1,
            },
        )
        if not inv_created:
            updated = False
            if inventory.stock != instance.stock:
                inventory.stock = instance.stock
                updated = True
            if (
                getattr(instance, "min_stock", None) is not None
                and inventory.min_stock != instance.min_stock
            ):
                inventory.min_stock = instance.min_stock
                updated = True
            if updated:
                inventory.save(update_fields=["stock", "min_stock"])
    except Exception as e:
        print("Inventory sync signal error:", e)
