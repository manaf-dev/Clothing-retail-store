from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, ProfileUpdateSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Get current user profile"""
    serializer = UserSerializer(request.user)
    data = serializer.data

    # Add staff profile data if exists
    if hasattr(request.user, "staff_profile"):
        from apps.staff.serializers import StaffProfileSerializer

        staff_data = StaffProfileSerializer(request.user.staff_profile).data
        data["staff_profile"] = staff_data

    return Response(data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Update current user profile"""
    serializer = ProfileUpdateSerializer(
        request.user, data=request.data, partial=True, context={"request": request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
