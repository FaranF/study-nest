from .models import *
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "slug", "courses_count"]
    courses_count = serializers.IntegerField(read_only=True)


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["title", "slug"]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "instructor",
            "category",
            "thumbnail",
            "created_at",
            "updated_at",
            "is_published",
        ]


class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["title", "description", "instructor", "category", "thumbnail"]


class CourseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["title", "description", "category", "thumbnail"]


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "order",
            "course",
            "content",
            "video_file",
            "created_at",
        ]


class LessonCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["title", "order", "course", "content", "video_file"]


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["id", "student", "course", "enrolled_at", "is_active"]


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["student", "course"]


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ["id", "enrollment", "lesson", "is_completed", "completed_at"]


class ProgressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ["enrollment", "lesson"]
