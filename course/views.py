from django.shortcuts import render

import course

# from .permissions import FullDjangoModelPermissions, IsAdminOrReadOnly, ViewCustomerHistoryPermission
from .pagination import DefaultPagination
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import (
    AllowAny,
    DjangoModelPermissions,
    DjangoModelPermissionsOrAnonReadOnly,
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from .filters import CourseFilter, LessonFilter, EnrollmentFilter, ProgressFilter
from .models import *
from .serializers import *


# Create your views here.
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(courses_count=Count("courses")).all()
    serializer_class = CategorySerializer
    pagination_class = DefaultPagination
    # permission_classes = [IsAdminOrReadOnly]
    search_fields = ["title"]
    ordering_fields = ["title"]


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter
    # permission_classes = [IsAdminOrReadOnly]
    search_fields = ["title"]
    ordering_fields = ["title"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CourseCreateSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return CourseUpdateSerializer
        return CourseSerializer


class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = LessonFilter
    # permission_classes = [IsAdminOrReadOnly]
    search_fields = ["title"]
    ordering_fields = ["title"]

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return LessonCreateUpdateSerializer
        return LessonSerializer


class EnrollmentViewSet(
    CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet
):
    queryset = Enrollment.objects.all()
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = EnrollmentFilter
    # permission_classes = [IsAdminOrReadOnly]
    search_fields = ["student", "course"]
    ordering_fields = ["student", "course"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return EnrollmentCreateSerializer
        return EnrollmentSerializer


class ProgressViewSet(
    CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet
):
    queryset = Progress.objects.all()
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProgressFilter
    # permission_classes = [IsAdminOrReadOnly]
    search_fields = ["enrollment", "lesson"]
    ordering_fields = ["enrollment", "lesson"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProgressCreateSerializer
        return ProgressSerializer
