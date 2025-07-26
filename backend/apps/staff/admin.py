from django.contrib import admin
from .models import StaffProfile

# Register your models here.


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role", "employee_id", "hire_date", "is_active"]
    list_filter = ["role", "is_active", "hire_date"]
    search_fields = ["user__username", "user__email", "employee_id"]
    ordering = ["-created_at"]
