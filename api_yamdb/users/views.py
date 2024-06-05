import random
from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.mail import send_mail
from django.core.cache import cache

from .serializers import SignupSerializer, TokenSerializer
from .models import UserModel
from core.constants import MIN_CODE, MAX_CODE


class SignupView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')
            confirmation_code = str(random.randint(MIN_CODE, MAX_CODE))

            cache_key = f'confirmation_code_{email}'
            cache.set(cache_key, confirmation_code, timeout=300)

            user, created = UserModel.objects.get_or_create(
                username=username,
                email=email
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
                {'message': 'Код подтверждения отправлен на указаную почту'},
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            confirmation_code = str(
                serializer.validated_data.get('confirmation_code')
            )
            # Получаем код подтверждения из кэша
            cache_key = f'confirmation_code_{email}'
            cached_code = cache.get(cache_key)
            if cached_code == confirmation_code:
                user = UserModel.objects.get(email=email)
                tokens = serializer.create(validated_data={'email': email})

                # Очистка кэша
                cache.delete(cache_key)
                return Response(tokens, status=status.HTTP_200_OK)
            return Response(
                {'error': 'Неверный код подтверждения'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
