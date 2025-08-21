from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.products"

    def ready(self):  # noqa: D401
        # Import signals to ensure inventory auto-sync is active
        try:
            from . import signals  # noqa: F401
        except Exception as e:
            # Avoid crashing app startup; replace with logging in production
            print("ProductsConfig.ready signal import error:", e)
