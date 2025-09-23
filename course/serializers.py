from django.apps import apps
from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "slug", "courses_count"]

    courses_count = serializers.IntegerField(read_only=True)


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["title", "slug"]


class InstructorSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    class Meta:
        model = apps.get_model(settings.USER_PROFILE)
        fields = ["role", "bio", "profile_image", "user_info"]

        
    def get_user_info(self, obj):
        return {
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
        }


class CourseSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer(read_only=True)
    lessons_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "instructor",
            "category",
            "lessons_count",
            "description",
            "thumbnail",
            "created_at",
            "updated_at",
            "is_published",
        ]


class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "description", "category", "thumbnail"]


class LessonSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(read_only=True)

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
    course = serializers.PrimaryKeyRelatedField(read_only=True)

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
