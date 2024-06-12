from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
<<<<<<< HEAD
from rest_framework import viewsets
=======
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions

>>>>>>> 85e76090129dbff2d0639b0b697b3de7de63dd33
from reviews.models import (
    Category, Genre, Title, Reviews)
from .serializers import (
<<<<<<< HEAD
    CategorySerializer, GenreSerializer, ReviewsSerializer,
    CommentSerializer, TitleGetSerializer, TitlePostSerializer, TitleSerializer
)
=======
    CategorySerializer,
    GenreSerializer,
    ReviewsSerializer,
    CommentSerializer,
    TitleGetSerializer,
    TitlePostSerializer,
    TitleSerializer)
>>>>>>> 85e76090129dbff2d0639b0b697b3de7de63dd33
from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissons import AdminOrReadOnly, IsOwnerOrReadOnly


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
    )

    def perform_create(self, serializer):
        title_id = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            title_id=title_id
        )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(
            Title,
            pk=title_id
        )
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
<<<<<<< HEAD


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = (AdminOrReadOnly, IsOwnerOrReadOnly)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        return Reviews.objects.all()
=======
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AdminOrReadOnly
    )

    def get_queryset(self):
        rewiew = get_object_or_404(
            Reviews,
            id=self.kwargs.get('rewiew_id')
        )
        return rewiew.comments.all

    def perform_create(self, serializer):
        review = get_object_or_404(
            Reviews,
            id=self.kwargs.get('review_id')
        )
        serializer.save(
            author=self.request.user,
            review=review
        )
>>>>>>> 85e76090129dbff2d0639b0b697b3de7de63dd33
