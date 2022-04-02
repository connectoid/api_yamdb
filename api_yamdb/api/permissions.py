from rest_framework import permissions
from django.conf import settings


class OwnerAdminModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            request.method in permissions.SAFE_METHODS or
            obj.author == request.user or
            user.is_admin or user.is_moderator
        )

class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser))
        )


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        role_list = settings.ROLE_CHOICES[2]
        return (request.method in permissions.SAFE_METHODS
                or request.user.role in role_list)

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (user.is_authenticated and user.is_admin
                or user.is_superuser)
