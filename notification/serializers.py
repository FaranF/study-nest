from models import *
from rest_framework import serializers


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "recipient",
            "message",
            "is_read",
            "object_id",
            "content_object",
            "created_at",
        ]


class NotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["recipient", "message", "object_id", "content_object"]


class NotificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["message", "is_read"]
