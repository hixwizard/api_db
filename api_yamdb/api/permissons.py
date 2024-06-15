from rest_framework import permissions


class IsAdminIsAuthOrReadOnly(permissions.BasePermission):
    """Доступ админу или только для чтения."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.is_admin or request.user.is_superuser)


class IsAuthorIsModeratorIsAdminIsAuthOrReadOnly(permissions.BasePermission):
    """Доступ автору или модератору или только для чтения."""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.user == obj.author
                     or request.user.is_moderator
                     or request.user.is_admin
                     or request.user.is_superuser
                     )
                )


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Разрешает доступ только аутентифицированным пользователям
    для выполнения операций записи (CREATE, PATCH, DELETE).
    Для запросов на чтение (GET) доступ разрешен для всех,
    включая неаутентифицированных пользователей.
    """
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated
            or request.method == 'GET'
        )


class AdminOnly(permissions.BasePermission):
    """Правада доступа для персонала."""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin
                or request.user.is_superuser)
