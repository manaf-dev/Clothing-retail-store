from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Customer
from .serializers import CustomerSerializer

# Create your views here.


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "email", "phone"]
    ordering_fields = ["name", "total_spent"]
