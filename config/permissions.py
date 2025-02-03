from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsSuperUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_superuser
        )


class IsCurrentUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj
