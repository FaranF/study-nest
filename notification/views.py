from ast import Not
from django.forms import ValidationError
from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *
from .permissions import *
from .pagination import DefaultPagination
from .filters import NotificationFilter

# Create your views here.

class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.select_related("recipient__user", "content_type")
    permission_classes = [NotificationPermission]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = NotificationFilter
    search_fields = ["message"]
    ordering_fields = ["is_read","created_at"]

    def get_serializer_class(self):
        if self.action == "create":
            return NotificationCreateSerializer

        if self.action in ["update", "partial_update"]:
            user = self.request.user
            obj = self.get_object()

            if user.is_staff or user.is_superuser:
                return NotificationUpdateAdminSerializer
            elif obj.recipient.user == user:
                return NotificationUpdateRecipientSerializer

        return NotificationSerializer

    def perform_create(self, serializer):
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            raise PermissionDenied("Only admins or staff can assign notifications.")

        serializer.save(
            recipient=serializer.validated_data.pop("recipient"),
            content_type=serializer.validated_data.pop("content_type_obj"),
        )

    def get_queryset(self):
        Profile = apps.get_model(settings.USER_PROFILE)
        try:
            profile = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            profile = None

        user = self.request.user
        if user.is_staff or user.is_superuser:
            return super().get_queryset()

        if profile:
            return super().get_queryset().filter(recipient=profile)

        return Notification.objects.none()
    
    
