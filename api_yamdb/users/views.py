import random
from rest_framework import status, views, viewsets, permissions
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
from core.constants import MIN_CODE, MAX_CODE


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
            if confirmation_code is None:
                return Response(
                    {'error': 'Отсутствует код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                return Response(
                    {'error': 'Пользователь с указанным именем не найден'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cached_code = cache.get(f'confirmation_code_{user.email}')
            if cached_code and cached_code == str(confirmation_code):
                tokens = serializer.create(validated_data={'username': username, 'confirmation_code': confirmation_code})
                # Очистка кэша
                cache.delete(f'confirmation_code_{user.email}')
                return Response(tokens, status=status.HTTP_200_OK)
            return Response(
                {'error': 'Неверный код подтверждения'},
                status=status.HTTP_400_BAD_REQUEST
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
