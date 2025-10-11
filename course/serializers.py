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


class RoleSerializer(serializers.ModelSerializer):
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
    instructor = RoleSerializer(read_only=True)
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
    student = RoleSerializer(read_only=True)
    course = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Enrollment
        fields = ["id", "student", "course", "enrolled_at", "is_active"]


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["course"]

    def validate(self, attrs):
        view = self.context.get("view")
        student = view.get_profile() if view else None
        course = attrs.get("course")

        if not student:
            raise serializers.ValidationError(
                {"non_field_errors": ["You must have a student profile to enroll."]}
            )

        if Enrollment.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError(
                {"non_field_errors": ["You are already enrolled in this course."]}
            )

        return attrs


class ProgressSerializer(serializers.ModelSerializer):
    enrollment = serializers.PrimaryKeyRelatedField(read_only=True)
    lesson = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Progress
        fields = ["id", "enrollment", "lesson", "is_completed", "completed_at"]


class ProgressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ["lesson"]

    def validate(self, attrs):
        lesson = attrs.get("lesson")
        enrollment_id = self.context.get("enrollment_id")

        if not enrollment_id:
            raise serializers.ValidationError(
                {"non_field_errors": ["Enrollment ID is required."]}
            )

        if Progress.objects.filter(enrollment_id=enrollment_id, lesson=lesson).exists():
            raise serializers.ValidationError(
                {"non_field_errors": ["You have already started this lesson."]}
            )

        return attrs
