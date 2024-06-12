from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import (
    Category, Genre, Title, Review, Comment)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    ReviewSerializer,
    CommentSerializer,
    TitleGetSerializer,
    TitlePostSerializer,
    TitleSerializer)
from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissons import AdminOrReadOnly, ReviewCommentPermission


class TitleViewSet(viewsets.ModelViewSet):
    """Набор названий."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitlePostSerializer

    def get_queryset(self):
        return Title.objects.all().annotate(
            rating=Avg('reviews__score')).order_by('id')


class CategoryViewSet(CreateListDestroyViewSet):
    """Набор категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    """Набор жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    '''Набор отзывов.'''
    serializer_class = ReviewSerializer
    permission_classes = (ReviewCommentPermission,)

    def get_queryset(self):
        return Title.objects.all(self.kwargs['title_id'])

    def get_object(self):
        return Title.objects.get(self.kwargs['title_id'])

    def perform_create(self, serializer):
        '''post'''
        return super().perform_create(serializer)

    def partial_update(self, request, *args, **kwargs):
        '''patch'''
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        '''delete'''
        return super().destroy(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    '''Набор комментариев.'''
    serializer_class = CommentSerializer
    permission_classes = (ReviewCommentPermission,)

    def get_queryset(self):
        return Review.objects.all(self.kwargs['title_id'])

    def get_object(self):
        return Review.objects.get(self.kwargs['title_id'])

    def perform_create(self, serializer):
        '''post'''
        return super().perform_create(serializer)

    def partial_update(self, request, *args, **kwargs):
        '''patch'''
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        '''delete'''
        return super().destroy(request, *args, **kwargs)
