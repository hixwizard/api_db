import random
import hashlib
from rest_framework import status, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from django.core.mail import send_mail
from django.core.cache import cache

from .serializers import (
    SignupSerializer, TokenSerializer,
    UserSerializer, UserCreateSerializer)
from .models import UserModel
from core.constants import MIN_CODE, MAX_CODE, EMAIL_MAX


class SignupView(views.APIView):
    """Представление для регистрации нового пользователя."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')
            confirmation_code = str(random.randint(MIN_CODE, MAX_CODE))

            # Сохраняем код подтверждения в кэше
            cache.set(
                f'confirmation_code_{email}',
                confirmation_code
            )

            user, created = UserModel.objects.get_or_create(
                username=username,
                defaults={'email': email}
            )
            if not created:
                user.confirmation_code = confirmation_code
                user.save()
            else:
                user.confirmation_code = confirmation_code
                user.save()
            send_mail(
                'Код подтверждения',
                f'Ваш код подтверждения {confirmation_code}',
                'noreply@example.com',
                [email],
                fail_silently=False,
            )
            return Response(
                {'message': 'Код подтверждения отправлен на указанную почту'},
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
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Проверка длины email
            if len(user.email) > EMAIL_MAX:
                return Response(
                    {'error': 'Email не может быть длиннее 254 символов.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            email_hash = hashlib.md5(user.email.encode()).hexdigest()
            cached_code = cache.get(f'confirmation_code_{email_hash}')

            if not cached_code or cached_code != str(confirmation_code):
                return Response(
                    {'error': 'Неверный код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Создаем токен
            tokens = serializer.create(
                validated_data={'username': username,
                                'confirmation_code': confirmation_code}
            )

            # Удаляем код подтверждения из кэша
            cache.delete(f'confirmation_code_{email_hash}')

            # Возвращаем информацию о пользователе и токенах
            return Response(
                {
                    'username': user.username,
                    'email': user.email,
                    'tokens': tokens
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(
    RetrieveModelMixin, UpdateModelMixin, GenericViewSet
):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
