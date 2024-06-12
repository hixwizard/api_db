from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import (
    Category, Genre, Title, Review)
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
from .permissons import AdminOrReadOnly


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
    permission_classes = ReviewSerializer

    def get_serializer_class(self):
        review = self.kwargs['id']
        return Review.objects.all(review=review)


class CommentViewSet(viewsets.ModelViewSet):
    '''Набор комментариев.'''
    serializer_class = CommentSerializer
    permission_classes = CommentSerializer
