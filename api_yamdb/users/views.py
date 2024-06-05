import random
from rest_framework import status, views, viewsets, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
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
                confirmation_code, timeout=300
            )
            user, crated = UserModel.objects.get_or_create(
                username=username,
                email=email
            )
            if not crated:
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
                {'message': 'Код подтверждения отправлен на указаную почту'},
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(views.APIView):
    """Представление для получения токена аутентификации."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            confirmation_code = serializer.validated_data.get(
                'confirmation_code'
            )
            # Получаем код подтверждения из кэша
            cached_code = cache.get(f'confirmation_code_{email}')
            if cached_code == confirmation_code:
                tokens = serializer.create(validated_data={'email': email})
                return Response(tokens, status=status.HTTP_200_OK)

            return Response({'error': 'Неверный код подтверждения'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Набор для выполнения CRUD операций с пользователем."""
    queryset = UserModel.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return self.serializer_class

    def get_queryset(self):
        if self.request.user.is_superuser:
            return UserModel.objects.all()
        return UserModel.objects.filter(username=self.request.user.username)
