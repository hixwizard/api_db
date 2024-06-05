from rest_framework.permissions import BasePermission


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Разрешает доступ только аутентифицированным пользователям
    для выполнения операций записи (создание, обновление, удаление).
    Для запросов на чтение (GET) доступ разрешен для всех,
    включая неаутентифицированных пользователей.
    """
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated
            or request.method == 'GET'
        )
