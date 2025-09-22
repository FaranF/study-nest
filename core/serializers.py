from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer,
)
from rest_framework import serializers
from .models import Profile, User


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ["username", "password", "email", "first_name", "last_name"]


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ["id", "username", "email", "first_name", "last_name"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "user", "role", "bio", "profile_image"]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    username = serializers.CharField(source="user.username")

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "role",
            "bio",
            "profile_image",
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()
        return instance


class RegisterProfileSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = Profile
        fields = ["user", "role", "bio", "profile_image"]
