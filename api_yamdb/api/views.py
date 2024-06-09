import random
import hashlib
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail
from django.core.cache import cache

from reviews.models import (
    Category, Genre, Title, Reviews, Comment
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    ReviewsSerializer,
    CommentSerializer,
    TitleGetSerializer,
    TitlePostSerializer,
    TitleSerializer
)
from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissons import AdminOrReadOnly
from .serializers import (
    SignupSerializer, TokenSerializer,
    UserCreateSerializer)
from users.models import UserModel
from core.constants import MIN_CODE, MAX_CODE


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
    """Набор отзывов."""
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Набор комментариев."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class SignupView(views.APIView):
    """Представление для регистрации нового пользователя."""
    permission_classes = (AllowAny,)

    def post(self, request):
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
                    {'detail': 'Пользователь с таким email уже зарегистрирован.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = str(random.randint(MIN_CODE, MAX_CODE))
            email_hash = hashlib.md5(email.encode()).hexdigest()
            cache.set(f'confirmation_code_{email_hash}', confirmation_code, timeout=3600)  # Срок действия 1 час

            user, created = UserModel.objects.get_or_create(
                username=username,
                defaults={'email': email}
            )

            if not created:
                user.email = email
                user.save()

            send_mail(
                'Код подтверждения',
                f'Ваш код подтверждения: {confirmation_code}',
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
    """Представление для получения токена аутентификации."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            confirmation_code = serializer.validated_data.get(
                'confirmation_code'
            )

            if not username or not confirmation_code:
                return Response(
                    {'error': 'Отсутствует имя или код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                return Response(
                    {'error': 'Пользователь с указанным именем не найден'},
                    status=status.HTTP_404_NOT_FOUND
                )
            email_hash = hashlib.md5(user.email.encode()).hexdigest()
            cached_code = cache.get(f'confirmation_code_{email_hash}')

            if not cached_code or cached_code != str(confirmation_code):
                return Response(
                    {'error': 'Неверный код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            tokens = serializer.create(
                validated_data={'username': username,
                                'confirmation_code': confirmation_code}
            )
            cache.delete(f'confirmation_code_{email_hash}')

            return Response(
                {
                    'username': user.username,
                    'email': user.email,
                    'tokens': tokens
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Набор отображений пользователей."""
    queryset = UserModel.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_object(self):
        return self.request.user

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
