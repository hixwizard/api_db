from rest_framework import filters, mixins, viewsets
from reviews.models import Review
from .permissons import AdminOrReadOnly


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Вьюсет позволяет делать GET, POST, DELETE запросы"""
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'


class CommentReviewMixin:
    def get_queryset(self):
        return Review.objects.all(self.kwargs['id'])

    def get_object(self):
        return Review.objects.get(self.kwargs['id'])

    def perform_create(self, serializer):
        '''post'''
        return super().perform_create(serializer)

    def partial_update(self, request, *args, **kwargs):
        '''patch'''
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        '''delete'''
        return super().destroy(request, *args, **kwargs)
