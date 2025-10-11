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
from .filters import ReviewFilter

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.select_related("reviewer__user", "content_type")
    permission_classes = [ReviewPermission]
    
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ReviewFilter
    search_fields = ["comment"]
    ordering_fields = ["rating"]


    def get_serializer_class(self):
        if self.action == "create":
            return ReviewCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return ReviewUpdateSerializer
        return ReviewSerializer

    def get_profile(self):
        if not hasattr(self, "_cached_profile"):
            Profile = apps.get_model(settings.USER_PROFILE)
            try:
                self._cached_profile = Profile.objects.get(user=self.request.user)
            except Profile.DoesNotExist:
                self._cached_profile = None
        return self._cached_profile

    def perform_create(self, serializer):
        reviewer = serializer.context.get('reviewer')
        content_type_obj = serializer.context.get('content_type_obj')

        if not reviewer:
            raise PermissionDenied("You must have a profile to leave a review.")

        serializer.save(
            reviewer=reviewer,
            content_type=content_type_obj,
        )            


    def get_queryset(self):
        queryset = super().get_queryset()

        content_type = self.request.query_params.get("content_type")
        object_id = self.request.query_params.get("object_id")

        if content_type and object_id:
            try:
                ct = ContentType.objects.get(model=content_type)
                queryset = queryset.filter(content_type=ct, object_id=object_id)
            except ContentType.DoesNotExist:
                return Review.objects.none()

        return queryset
