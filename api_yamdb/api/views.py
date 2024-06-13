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
    serializer_class = ReviewsSerializer
    permission_classes = (
        IsAuthorIsModeratorIsAdminOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    )
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        title_id = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            title_id=title_id
        )
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(
            Title,
            pk=title_id
        )
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    '''Набор комментариев.'''
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorIsModeratorIsAdminOrReadOnly
    )
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        rewiew = get_object_or_404(
            Reviews,
            pk=self.kwargs.get('review_id')
        )
        return rewiew.comments.all()

    def perform_create(self, serializer):
        review_id = get_object_or_404(
            Reviews,
            pk=self.kwargs.get('review_id')
        )
        title_id = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        serializer.save(
            title_id=title_id,
            author=self.request.user,
            review_id=review_id,
        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
