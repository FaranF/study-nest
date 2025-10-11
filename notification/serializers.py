from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .models import *

class RecipientSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = apps.get_model(settings.USER_PROFILE)
        fields = ["role", "user_info"]

    def get_user_info(self, obj):
        return {
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
        }

class NotificationSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()
    recipient = RecipientSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            "id",
            "recipient",
            "message",
            "is_read",
            "object_id",
            "content_type",
            "created_at",
        ]

    def get_content_type(self, obj):
        return obj.content_type.model


class NotificationUpdateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["message"]


class NotificationUpdateRecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["is_read"]


class NotificationCreateSerializer(serializers.ModelSerializer):
    content_type_id = serializers.IntegerField(write_only=True)
    recipient = serializers.PrimaryKeyRelatedField(
        queryset=apps.get_model(settings.USER_PROFILE).objects.select_related("user").all()
    )

    class Meta:
        model = Notification
        fields = ["id", "message", "object_id", "content_type_id", "recipient"]

    def validate_content_type_id(self, value):
        try:
            ct = ContentType.objects.get(id=value)
        except ContentType.DoesNotExist:
            raise serializers.ValidationError("Invalid content_type_id.")
        return ct

    def validate(self, attrs):
        recipient = attrs.get("recipient")
        ct = attrs.pop("content_type_id")
        object_id = attrs.get("object_id")
        message = attrs.get("message")

        if Notification.objects.filter(
            recipient=recipient,
            content_type=ct,
            object_id=object_id,
            message=message,
        ).exists():
            raise serializers.ValidationError(
                {"non_field_errors": ["This notification already exists."]}
            )

        attrs["content_type_obj"] = ct
        return attrs
