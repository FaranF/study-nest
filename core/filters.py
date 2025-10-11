from django_filters.rest_framework import FilterSet
from . import models


class ProfileFilter(FilterSet):
    class Meta:
        model = models.Profile
        fields = {
            "role": ["exact"],
        }
