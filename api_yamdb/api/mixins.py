from rest_framework import mixins, viewsets

from .permissons import AdminOrReadOnly


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Вьюсет позволяет делать GET, POST, DELETE запросы"""
    search_fields = ('name',)
    permission_classes = AdminOrReadOnly
