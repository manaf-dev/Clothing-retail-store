from django.urls import path
from . import views

urlpatterns = [
    path("overview/", views.dashboard_overview, name="dashboard-overview"),
    path("sales-summary/", views.sales_summary, name="sales-summary"),
    path("inventory-alerts/", views.inventory_alerts, name="inventory-alerts"),
]
