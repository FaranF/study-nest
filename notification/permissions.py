from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied

from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class NotificationPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return request.user.is_authenticated

        if request.method == "POST":
            return request.user.is_staff or request.user.is_superuser

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return user.is_staff or user.is_superuser or obj.recipient.user == user

        if request.method in ["PUT", "PATCH", "DELETE"]:
            if user.is_staff or user.is_superuser or obj.recipient.user == user:
                return True

        return False
