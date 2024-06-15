import random
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from django.core.cache import cache
from rest_framework import viewsets, permissions, status, views, viewsets


from reviews.models import (
    Category, Genre, Title, Review)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    ReviewsSerializer,
    CommentSerializer,
    TitleGetSerializer,
    TitlePostSerializer,
    SignupSerializer,
    TokenSerializer,
    UserSerializer,
    UserCreateSerializer
)
from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissons import (
    IsAdminIsAuthOrReadOnly,
    IsAuthorIsModeratorIsAdminIsAuthOrReadOnly,
    AdminOnly,
    IsAuthenticatedOrReadOnly)
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from users.models import UserModel
from core.constants import MIN_CODE, MAX_CODE, FIVE_MIN


class TitleViewSet(viewsets.ModelViewSet):
    """Представление произведений."""
    permission_classes = (IsAdminIsAuthOrReadOnly, IsAuthenticatedOrReadOnly)
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
    """Представление категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    """Представление жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление отзывов."""
    serializer_class = ReviewsSerializer
    permission_classes = (
        IsAuthorIsModeratorIsAdminIsAuthOrReadOnly,
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

    def get_queryset(self):
        title = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title)
        return title.reviews.all().order_by('id')


class CommentViewSet(viewsets.ModelViewSet):
    """Представление комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorIsModeratorIsAdminIsAuthOrReadOnly,
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


class SignupView(views.APIView):
    """Запрос регистрации и ответ с кодом аутентификации."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        email = request.data.get('email')
        username = request.data.get('username')
        if UserModel.objects.filter(email=email).exists():
            if UserModel.objects.filter(username=username).exists():
                return Response(
                    {'detail': 'Пользователь уже зарегистрирован.'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'detail':
                     'Пользователь с таким email уже зарегистрирован.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')
            confirmation_code = str(random.randint(MIN_CODE, MAX_CODE))
            cache_key = f'confirmation_code_{username}'
            cache.set(cache_key, confirmation_code, timeout=FIVE_MIN)
            user, created = UserModel.objects.get_or_create(
                username=username,
                email=email
            )
            if not created:
                user.email = email
                user.save()
            user.confirmation_code = confirmation_code
            user.save()
            send_mail(
                'Код подтверждения для входа.',
                f'Ваш код подтверждения {confirmation_code}',
                'noreply@example.com',
                [email],
                fail_silently=False,
            )
            return Response(
                {'username': user.username, 'email': user.email},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(views.APIView):
    """Получение токена по коду подтверждения."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            confirmation_code = str(
                serializer.validated_data.get('confirmation_code')
            )
            cache_key = f'confirmation_code_{username}'
            cached_code = cache.get(cache_key)
            if not username or not confirmation_code:
                return Response(
                    {'error': 'Отсутствует имя или код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                return Response(
                    {'error': 'Пользователь с указанным именем не найден'},
                    status=status.HTTP_404_NOT_FOUND
                )
            if cached_code == confirmation_code:
                UserModel.objects.get(username=username)
                tokens = serializer.create(
                    validated_data={'username': username}
                )
                cache.delete(cache_key)
                return Response(tokens, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Неверный код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Представление пользователей."""
    queryset = UserModel.objects.all()
    serializer_class = UserCreateSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    permission_classes = (AdminOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(methods=['get', 'patch'], detail=False, url_path='me',
            permission_classes=(IsAuthenticated,))
    def get_my_profile(self, request):
        serializer = UserSerializer(request.user, partial=True,
                                    data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.method == 'PATCH':
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
