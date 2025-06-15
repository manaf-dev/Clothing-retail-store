from django.contrib import admin
from .models import Supplier, Inventory, RestockHistory

admin.site.register(Supplier)
admin.site.register(Inventory)
admin.site.register(RestockHistory)
# Register your models here.
