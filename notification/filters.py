from django_filters.rest_framework import FilterSet, filters

from .models import Notification

class NotificationFilter(FilterSet):
    class Meta:
        model = Notification
        fields = {
            "object_id": ["exact"],
            "is_read": ["exact"],
            "created_at": ["date", "year", "month"],
        }

