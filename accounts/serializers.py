from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
        )


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
        )

        return user

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        email = data["email"]
        password = data["password"]

        user = authenticate(
            email=email,
            password=password,
        )

        if user is None:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        data["user"] = user

        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context["request"].user

        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")

        return value

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters."
            )

        return value

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()