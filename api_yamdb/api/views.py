from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from reviews.models import (
    Category, Genre, Title, Review)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    ReviewsSerializer,
    CommentSerializer,
    TitleGetSerializer,
    TitlePostSerializer,
    TitleSerializer)
from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissons import AdminOrReadOnly, IsAuthorIsModeratorIsAdminOrReadOnly


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
    serializer_class = ReviewsSerializer
    permission_classes = (
        IsAuthorIsModeratorIsAdminOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    )
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            title=title
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        title = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title)
        return title.reviews.all().order_by('id')


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorIsModeratorIsAdminOrReadOnly,
    )
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id')
        )
        return review.comments.all().order_by('id')

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id')
        )
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        serializer.save(
            title=title,
            author=self.request.user,
            review=review,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
