from rest_framework.permissions import BasePermission
from rest_framework import permissions


class AdminOrReadOnly(BasePermission):
    """Доступ админу или только для чтения."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.is_admin or request.user.is_superuser)


class ReviewCommentPermission(BasePermission):
    '''Доступ авторизованному пользователю или для персонала.'''
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS
            or obj.author == request.user):
            return True
        return (
            request.user.is_authenticated
            and (request.user.is_moderator or request.user.is_admin))
