from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from .serializers import StaffSerializer, CreateStaffSerializer

# Create your views here.


class StaffViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter().select_related("staff_profile")
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        Only admins can create, update, delete staff. Others can only view.
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateStaffSerializer
        return StaffSerializer

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        """Deactivate a staff member"""
        staff = self.get_object()
        staff.is_active = False
        staff.save()

        # Also deactivate staff profile
        if hasattr(staff, "staff_profile"):
            staff.staff_profile.is_active = False
            staff.staff_profile.save()

        return Response({"message": "Staff member deactivated successfully"})

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        """Activate a staff member"""
        staff = self.get_object()
        staff.is_active = True
        staff.save()

        # Also activate staff profile
        if hasattr(staff, "staff_profile"):
            staff.staff_profile.is_active = True
            staff.staff_profile.save()

        return Response({"message": "Staff member activated successfully"})

    @action(detail=False, methods=["get"])
    def roles(self, request):
        """Get available staff roles"""
        from .models import ROLE_CHOICES

        return Response(
            [{"value": choice[0], "label": choice[1]} for choice in ROLE_CHOICES]
        )
