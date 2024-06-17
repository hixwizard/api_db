from rest_framework import permissions


class IsAdminOnly(permissions.BasePermission):
    """Доступ только админу."""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin
                or request.user.is_superuser)


class IsAdminIsAuthOrReadOnly(IsAdminOnly):
    """Доступ админу или только для чтения."""

    def has_permission(self, request, view):
        return (super().has_permission(request, view)
                or request.method in permissions.SAFE_METHODS)


class IsAuthorIsModeratorIsAdminIsAuthOrReadOnly(permissions.BasePermission):
    """Доступ автору, админу, модератору или только для чтения."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user == obj.author
                    or request.user.is_moderator
                    or request.user.is_admin
                    or request.user.is_superuser
                    )
                )
