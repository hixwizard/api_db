from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from reviews.models import (
    Category, Genre, Title, Reviews, Comment
)
from .serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer, ReviewsSerializer, CommentSerializer
)
from .mixins import CreateListDestroyViewSet
from .permissons import AdminOrReadOnly


class AuthViewSet(viewsets.ModelViewSet):
    pass


# class UserViewSet(viewsets.ModelViewSet):


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
