from django.db import models
from django.contrib.auth.models import User

# Create your models here.

ROLE_CHOICES = [
    ("admin", "Administrator"),
    ("manager", "Manager"),
    ("cashier", "Cashier"),
    ("sales_associate", "Sales Associate"),
]


class StaffProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="staff_profile"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="cashier")
    employee_id = models.CharField(max_length=10, unique=True)
    hire_date = models.DateField()
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_role_display()}"

    class Meta:
        ordering = ["-created_at"]
