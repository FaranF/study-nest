from ast import Is
from operator import is_
from django.db.models.aggregates import Count
from django.db.models import Count, Q
from django.forms import ValidationError
from django.shortcuts import render
from django.apps import apps
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.core.cache import cache

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
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.cache import cache_page

from .models import *
from .serializers import *
from .pagination import DefaultPagination
from .filters import CourseFilter, LessonFilter, EnrollmentFilter, ProgressFilter
from .permissions import (
    IsAdminOrReadOnly,
    IsInstructor,
    IsInstructorOrReadOnly,
    IsStudent,
)

import logging
logger = logging.getLogger(__name__)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(courses_count=Count("courses")).all()
    serializer_class = CategorySerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ["title"]
    ordering_fields = ["title"]


class CourseViewSet(ModelViewSet):
    queryset = (
        Course.objects.select_related("instructor", "instructor__user", "category")
        .annotate(lessons_count=Count("lessons"))
        .all()
    )

    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ["title"]
    ordering_fields = ["title"]
    permission_classes = [IsInstructorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH", "POST"]:
            return CourseCreateUpdateSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        Profile = apps.get_model(settings.USER_PROFILE)
        try:
            profile = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            raise PermissionDenied("You must have a profile to create/edit a course.")

        if profile.role != "I":
            raise PermissionDenied("Only instructors can create/edit courses.")

        course = serializer.save(instructor=profile)
        logger.info(f"Course '{course.title}' created by instructor {profile.id}")


    @action(detail=False, methods=["get"], permission_classes=[IsInstructor])
    def my_courses(self, request):
        profile = getattr(request, "profile", None)
        if profile is None:
            return Response(
                ["You must have a profile to view your courses."],
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = self.get_queryset().filter(instructor=profile)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = LessonFilter
    search_fields = ["title"]
    ordering_fields = ["title"]
    permission_classes = [IsInstructorOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.kwargs.get("course_pk")
        if course_id is not None:
            queryset = queryset.filter(course_id=course_id)
        return queryset

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH", "POST"]:
            return LessonCreateUpdateSerializer
        return LessonSerializer

    def perform_create(self, serializer):
        Profile = apps.get_model(settings.USER_PROFILE)
        try:
            profile = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            raise PermissionDenied("You must have a profile to create/edit a lesson.")

        course_id = self.kwargs.get("course_pk")
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            raise ValidationError("Invalid course ID in URL.")

        if course.instructor != profile:
            raise PermissionDenied("You can only add/edit lessons to your own courses.")

        # serializer.save(course=course)
        lesson = serializer.save(course=course)
        cache.clear() 
        return lesson
    
    @method_decorator(cache_page(60 * 10))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)



class EnrollmentViewSet(ModelViewSet):
    queryset = Enrollment.objects.all()
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = EnrollmentFilter
    permission_classes = [IsStudent | IsAdminUser]
    search_fields = ["student", "course"]
    ordering_fields = ["student", "course"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return EnrollmentCreateSerializer
        return EnrollmentSerializer

    def get_profile(self):
        if not hasattr(self, "_cached_profile"):
            Profile = apps.get_model(settings.USER_PROFILE)
            try:
                self._cached_profile = Profile.objects.get(user=self.request.user)
            except Profile.DoesNotExist:
                self._cached_profile = None
        return self._cached_profile

    def perform_create(self, serializer):
        profile = self.get_profile()
        if not profile:
            raise PermissionDenied("You must have a profile to create an enrollment.")
        if profile.role != "S":
            raise PermissionDenied("Only students can enroll in courses.")
        serializer.save(student=profile)

    def get_permissions(self):
        if self.action == "create":
            return [IsStudent()]
        return super().get_permissions()

    def get_queryset(self):
        profile = self.get_profile()
        queryset = Enrollment.objects.select_related(
            "student__user", "course__instructor__user", "course__category"
        )

        if self.request.user.is_staff:
            return queryset.all()

        if profile and profile.role == "S":
            return queryset.filter(student=profile)

        raise PermissionDenied("You don't have permission to access this progress.")


class ProgressViewSet(ModelViewSet):
    queryset = Progress.objects.all()
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProgressFilter
    permission_classes = [IsStudent | IsAdminUser]
    search_fields = ["enrollment", "lesson"]
    ordering_fields = ["enrollment", "lesson"]

    def get_serializer_class(self):
        if self.request.method in ["POST"]:
            return ProgressCreateSerializer
        return ProgressSerializer

    def get_profile(self):
        if not hasattr(self, "_cached_profile"):
            Profile = apps.get_model(settings.USER_PROFILE)
            try:
                self._cached_profile = Profile.objects.get(user=self.request.user)
            except Profile.DoesNotExist:
                self._cached_profile = None
        return self._cached_profile

    def perform_create(self, serializer):
        enrollment_id = self.kwargs.get("enrollment_pk")
        Enrollment = apps.get_model("course", "Enrollment")

        try:
            enrollment = Enrollment.objects.select_related("student__user").get(
                id=enrollment_id
            )
        except Enrollment.DoesNotExist:
            raise PermissionDenied("Enrollment does not exist.")

        profile = self.get_profile()
        if not profile:
            raise PermissionDenied("You must have a profile to create progress.")

        if not self.request.user.is_staff and enrollment.student != profile:
            raise PermissionDenied("You can only add progress for your own enrollment.")

        serializer.save(enrollment=enrollment)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["enrollment_id"] = self.kwargs.get("enrollment_pk")
        return context

    def get_permissions(self):
        if self.action == "create":
            return [IsStudent()]
        return super().get_permissions()

    def get_queryset(self):
        profile = self.get_profile()
        enrollment_id = self.kwargs.get("enrollment_pk")

        queryset = Progress.objects.select_related(
            "enrollment__student__user", "lesson", "enrollment__course"
        )

        if self.request.user.is_staff:
            return queryset.filter(enrollment_id=enrollment_id)

        try:
            enrollment = Enrollment.objects.get(id=enrollment_id)
        except Enrollment.DoesNotExist:
            raise PermissionDenied("Enrollment does not exist.")

        if enrollment.student == profile:
            return queryset.filter(enrollment_id=enrollment_id)

        raise PermissionDenied("You don't have permission to access this progress.")
