from django_filters.rest_framework import FilterSet, filters

from . import models


class CourseFilter(FilterSet):
    lessons_count__gt = filters.NumberFilter(field_name="lessons_count", lookup_expr="gt", label="Lessons count greater than")
    lessons_count__lt = filters.NumberFilter(field_name="lessons_count", lookup_expr="lt", label="Lessons count less than")
    class Meta:
        model = models.Course
        fields = {
            "category_id": ["exact"],
            "created_at": ["date", "year", "month"],
            "updated_at": ["date", "year", "month"],
            "is_published": ["exact"],
        }


class LessonFilter(FilterSet):
    class Meta:
        model = models.Lesson
        fields = {
            "order": ["gt", "lt"],
            "created_at": ["date", "year", "month"],
        }


class EnrollmentFilter(FilterSet):
    class Meta:
        model = models.Enrollment
        fields = {
            "enrolled_at": ["date", "year", "month"],
            "is_active": ["exact"],
        }


class ProgressFilter(FilterSet):
    class Meta:
        model = models.Progress
        fields = {
            "completed_at": ["date", "year", "month"],
            "is_completed": ["exact"],
        }
