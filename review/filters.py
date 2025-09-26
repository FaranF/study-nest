from django_filters.rest_framework import FilterSet, filters

from .models import Review

class ReviewFilter(FilterSet):
    class Meta:
        model = Review
        fields = {
            "object_id": ["exact"],
            "created_at": ["date", "year", "month"],
            "rating": ["gt", "lt"],
        }

