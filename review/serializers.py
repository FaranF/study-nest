from models import *
from rest_framework import serializers


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",
            "reviewer",
            "rating",
            "comment",
            "object_id",
            "content_object",
            "created_at",
        ]


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["reviewer", "rating", "comment", "object_id", "content_object"]


class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
