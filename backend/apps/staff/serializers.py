from rest_framework import serializers
from django.contrib.auth.models import User
from .models import StaffProfile
from django.contrib.auth.password_validation import validate_password


class StaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffProfile
        fields = [
            "role",
            "employee_id",
            "hire_date",
            "phone",
            "address",
            "salary",
            "is_active",
        ]


class StaffSerializer(serializers.ModelSerializer):
    staff_profile = StaffProfileSerializer(required=False)
    password = serializers.CharField(
        write_only=True, required=False, validators=[validate_password]
    )
    full_name = serializers.SerializerMethodField()

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
            "staff_profile",
            "password",
            "full_name",
        ]

    def get_full_name(self, obj):
        return obj.get_full_name() if obj.get_full_name() else obj.username

    def create(self, validated_data):
        staff_profile_data = validated_data.pop("staff_profile", {})
        password = validated_data.pop("password")

        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()

        StaffProfile.objects.create(user=user, **staff_profile_data)
        return user

    def update(self, instance, validated_data):
        staff_profile_data = validated_data.pop("staff_profile", {})
        password = validated_data.pop("password", None)

        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()

        # Update or create staff profile
        staff_profile, created = StaffProfile.objects.get_or_create(user=instance)
        for attr, value in staff_profile_data.items():
            setattr(staff_profile, attr, value)
        staff_profile.save()

        return instance


class CreateStaffSerializer(serializers.ModelSerializer):
    staff_profile = StaffProfileSerializer()
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "staff_profile",
            "password",
            "password2",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        staff_profile_data = validated_data.pop("staff_profile")
        validated_data.pop("password2")
        password = validated_data.pop("password")

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        StaffProfile.objects.create(user=user, **staff_profile_data)
        return user
