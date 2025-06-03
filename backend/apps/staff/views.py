from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import StaffSerializer

# Create your views here.


class StaffViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = StaffSerializer
