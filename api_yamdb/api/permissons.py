from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Доступ админу или только для чтения."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.is_admin or request.user.is_superuser)


class IsAuthorIsModeratorIsAdminOrReadOnly(permissions.BasePermission):
    """Доступ автору или модератору или только для чтения."""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.user == obj.author
                     or request.user.role == 'moderator'
                     or request.user.is_admin
                     or request.user.is_superuser
                     )
                )
