import random
import hashlib
from rest_framework import status, views, viewsets
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
    permission_classes = (AllowAny,)

    def post(self, request):
        print("Received signup request data:", request.data)
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
                status=status.HTTP_200_OK)
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
