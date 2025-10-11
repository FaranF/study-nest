from queue import Empty
from django.contrib import admin
from django.db.models.query import QuerySet
from datetime import date, timedelta
from . import models
from django.urls import reverse
from django.utils.html import format_html, urlencode
from django.db.models.aggregates import Count
from django.db.models import Q

class DateFilter(admin.SimpleListFilter):
    title = "date"
    parameter_name = "date_range"

    def lookups(self, request, model_admin):
        return [
            ("<2020", "Before 2020"),
            ("2020-2021", "2020 to 2021"),
            ("2021-2022", "2021 to 2022"),
            ("2022-2023", "2022 to 2023"),
            ("2023-2024", "2023 to 2024"),
            ("2024-2025", "2024 to 2025"),
            (">2025", "After 2025"),
        ]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset

        fields = [f.name for f in queryset.model._meta.get_fields()]

        candidate_fields = [
            "created_at",
            "updated_at",
            "enrolled_at",
            "completed_at",
        ]

        valid_fields = [f for f in candidate_fields if f in fields]

        if not valid_fields:
            return queryset

        q = Q()

        if self.value() == "<2020":
            for f in valid_fields:
                q |= Q(**{f + "__lt": date(2020, 1, 1)})

        elif self.value() == "2020-2021":
            for f in valid_fields:
                q |= Q(**{f + "__range": (date(2020, 1, 1), date(2020, 12, 31))})

        elif self.value() == "2021-2022":
            for f in valid_fields:
                q |= Q(**{f + "__range": (date(2021, 1, 1), date(2021, 12, 31))})

        elif self.value() == "2022-2023":
            for f in valid_fields:
                q |= Q(**{f + "__range": (date(2022, 1, 1), date(2022, 12, 31))})

        elif self.value() == "2023-2024":
            for f in valid_fields:
                q |= Q(**{f + "__range": (date(2023, 1, 1), date(2023, 12, 31))})

        elif self.value() == "2024-2025":
            for f in valid_fields:
                q |= Q(**{f + "__range": (date(2024, 1, 1), date(2024, 12, 31))})

        elif self.value() == ">=2025":
            for f in valid_fields:
                q |= Q(**{f + "__gt": date(2025, 12, 31)})

        return queryset.filter(q)

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    autocomplete_fields = ["featured_course"]
    list_display = ["title", "courses_count"]
    search_fields = ["title"]

    @admin.display(ordering=["featured_course"])
    def courses_count(self, category):
        url = (
            reverse("admin:course_course_changelist")
            + "?"
            + urlencode({"category__id": str(category.id)})
        )
        return format_html('<a href="{}">{} Courses</a>', url, category.featured_course)
    
    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                courses_count=Count("featured_course", distinct=True),
            )
        )
        
        
@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    autocomplete_fields = ["category", "instructor"]
    search_fields = ["title"]
    list_display = [
        "title",
        "description",
        "instructor",
        "category",
        "created_at",
        "updated_at",
        "is_published",
    ]
    list_editable = ["is_published"]
    list_per_page = 10
    list_filter = [
        "category",
        DateFilter,
        "is_published",
    ]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category", "instructor__user")
    
    
@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    autocomplete_fields = ["course"]
    search_fields = ["title"]
    list_display = [
        "title",
        "order",
        "course",
        "created_at",
    ]
    list_editable = ["order"]
    list_per_page = 10
    list_filter = [
        "order",
        DateFilter,
    ]
    readonly_fields = ['video']
    
    def video(self, instance):
        """Display the uploaded video file in admin as an HTML video player."""
        if instance.video_file:
            return format_html(
                '<video controls>'
                '<source src="{}" type="video/mp4">'
                'Your browser does not support the video tag.'
                '</video>',
                instance.video_file.url
            )
        return "No video uploaded"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("course")

    class Media:
        css = {
            "all": ("course/styles.css")
        }

@admin.register(models.Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    autocomplete_fields = ["student", "course"]
    search_fields = ["student", "course"]
    list_display = [
        "student",
        "course",
        "enrolled_at",
        "is_active",
    ]
    list_editable = ["is_active"]
    list_per_page = 10
    list_filter = [
        "is_active",
        DateFilter,
    ]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("course", "student__user")
    
    
@admin.register(models.Progress)
class ProgressAdmin(admin.ModelAdmin):
    autocomplete_fields = ["enrollment", "lesson"]
    search_fields = ["enrollment", "lesson"]
    list_display = [
        "enrollment",
        "lesson",
        "is_completed",
        "completed_at",
    ]
    list_editable = ["is_completed"]
    list_per_page = 10
    list_filter = [
        "is_completed",
        DateFilter,
    ]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("enrollment", "lesson")
