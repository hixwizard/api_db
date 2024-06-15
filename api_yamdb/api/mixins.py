from rest_framework import filters, mixins, viewsets, permissions

from .permissons import IsAdminIsAuthOrReadOnly

from core.constants import USERNAME_MAX_LENGTH, EMAIL_MAX


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Вьюсет позволяет делать GET, POST, DELETE запросы"""
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (
        IsAdminIsAuthOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly)
    lookup_field = 'slug'


class ExtraKwargsMixin:
    """Миксин валидации пользователей."""
    class Meta:
        extra_kwargs = {
            'username': {'max_length': USERNAME_MAX_LENGTH},
            'email': {'max_length': EMAIL_MAX, 'validators': []},
            'first_name': {'max_length': USERNAME_MAX_LENGTH},
            'last_name': {'max_length': USERNAME_MAX_LENGTH},
            'bio': {'allow_blank': True},
            'role': {'allow_blank': True},
        }
