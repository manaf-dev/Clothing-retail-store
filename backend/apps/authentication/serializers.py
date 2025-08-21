from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
        ]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def update(self, instance, validated_data):
        # Basic user field updates
        for field in ["username", "first_name", "last_name", "email"]:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        instance.save()

        # Handle optional staff profile updates like profile_image
        profile_image = (
            self.context.get("request").FILES.get("profile_image")
            if self.context.get("request")
            else None
        )
        if profile_image and hasattr(instance, "staff_profile"):
            instance.staff_profile.profile_image = profile_image
            instance.staff_profile.save(update_fields=["profile_image"])
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user
