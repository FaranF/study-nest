from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .models import *

class ReviewSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "id",
            "reviewer",
            "rating",
            "comment",
            "object_id",
            "content_type",
            "created_at",
        ]

    def get_content_type(self, obj):
        return obj.content_type.model


class ReviewCreateSerializer(serializers.ModelSerializer):
    content_type_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = ["id", "rating", "comment", "object_id", "content_type_id"]

    def validate(self, attrs):
        view = self.context.get("view")
        reviewer = view.get_profile() if view else None
        if not reviewer:
            raise PermissionDenied("You must have a profile to leave a review.")

        content_type_id = attrs.get("content_type_id")
        object_id = attrs.get("object_id")
        if not content_type_id:
            raise serializers.ValidationError({"content_type_id": "This field is required."})

        try:
            ct = ContentType.objects.get(id=content_type_id)
        except ContentType.DoesNotExist:
            raise serializers.ValidationError({"content_type_id": "Invalid content type id."})

        if Review.objects.filter(reviewer=reviewer, content_type=ct, object_id=object_id).exists():
            raise serializers.ValidationError(
                {"non_field_errors": ["You have already reviewed this object."]}
            )

        self.context['reviewer'] = reviewer
        self.context['content_type_obj'] = ct

        return attrs

class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
