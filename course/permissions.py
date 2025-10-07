from django.conf import settings
from django.apps import apps
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import Progress, Enrollment


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsInstructorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        Profile = apps.get_model(settings.USER_PROFILE)
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return False

        if hasattr(obj, "instructor"):
            return obj.instructor == profile
        if hasattr(obj, "course"):
            return obj.course.instructor == profile
        return False


class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to access this endpoint.")

        Profile = apps.get_model(settings.USER_PROFILE)
        try:
            request.profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            if not request.user.is_staff:
                raise PermissionDenied(
                    "You must have a profile to access this endpoint."
                )

        if not request.user.is_staff and request.profile.role != "I":
            raise PermissionDenied("Only instructors can access this endpoint.")

        return True


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to access this endpoint.")

        Profile = apps.get_model(settings.USER_PROFILE)
        try:
            request.profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            if not request.user.is_staff:
                raise PermissionDenied(
                    "You must have a profile to access this endpoint."
                )

        if not request.user.is_staff and request.profile.role != "S":
            raise PermissionDenied("Only students can access this endpoint.")

        return True
