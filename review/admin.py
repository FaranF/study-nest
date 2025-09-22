from django.contrib import admin
from . import models
from django.db.models import Q
from datetime import date
# Register your models here.

class DateFilter(admin.SimpleListFilter):
    title = "date"
    parameter_name = "date_range"  # single query param

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


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    autocomplete_fields = ["reviewer"]
    search_fields = [
        "reviewer__user__first_name",
        "reviewer__user__last_name",
        "comment",
    ]
    list_display = [
        "reviewer",
        "content_type_id",
        "object_id",
        "rating",
        "created_at",
    ]
    list_per_page = 10
    list_filter = [
        "rating",
        DateFilter,
    ]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("reviewer__user")
        )