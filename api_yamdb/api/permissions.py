from rest_framework import permissions


class OwnerAdminModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == user or user.is_admin or user.is_moderator
        )


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin
                or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated and request.user.is_admin
                or request.user.is_superuser
            )
        )


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (user.is_authenticated and user.is_admin
                or user.is_superuser)

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (user.is_authenticated and user.is_admin
                or user.is_superuser)
