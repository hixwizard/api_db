import random
import hashlib
from rest_framework import status, views, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
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
from .permissions import AdminOnly


class SignupView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        print("Received signup request data:", request.data)
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
                    {'detail': 'Пользователь с таким email уже зарегистрирован.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')
            confirmation_code = str(random.randint(MIN_CODE, MAX_CODE))

            cache_key = f'confirmation_code_{username}'
            cache.set(cache_key, confirmation_code, timeout=300)
            print(f"Cached confirmation code {confirmation_code} for user {username}")

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
                'Код подтверждения',
                f'Ваш код подтверждения {confirmation_code}',
                'noreply@example.com',
                [email],
                fail_silently=False,
            )
            return Response(
                {'username': user.username, 'email': user.email},
                status=status.HTTP_200_OK
            )
        else:
            print("Signup serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TokenView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            confirmation_code = str(serializer.validated_data.get('confirmation_code'))

            # Получаем код подтверждения из кэша
            cache_key = f'confirmation_code_{username}'
            cached_code = cache.get(cache_key)
            print(f"Cache key: {cache_key}")
            print(f"Cached code: {cached_code}, Type: {type(cached_code)}")
            print(f"Confirmation code: {confirmation_code}, Type: {type(confirmation_code)}")
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

            if cached_code == confirmation_code:
                user = UserModel.objects.get(username=username)
                tokens = serializer.create(validated_data={'username': username})

                # Очистка кэша
                cache.delete(cache_key)
                return Response(tokens, status=status.HTTP_200_OK)
            else:
                print(f"Invalid confirmation code. Expected: {cached_code}, Received: {confirmation_code}")
                return Response(
                    {'error': 'Неверный код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserViewSet(viewsets.ModelViewSet):
    """Набор отображений пользователей."""
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
