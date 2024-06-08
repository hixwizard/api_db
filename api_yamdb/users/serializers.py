from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from django.core.validators import RegexValidator

from .models import UserModel
from core.constants import USERNAME_MAX_LENGTH, MAX_CODE, EMAIL_MAX, MESSAGE


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации новых пользователей."""
    email = serializers.EmailField()
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=USERNAME_MAX_LENGTH,
        error_messages={
            'invalid': MESSAGE
        }
    )

    class Meta:
        model = UserModel
        fields = ('email', 'username')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Имя "me" уже занято.')
        return value

    def validate_email(self, value):
        if len(value) > EMAIL_MAX:
            raise serializers.ValidationError(
                'Email не может быть длиннее 254 символов.'
            )
        return value

    def validate(self, data):
        if UserModel.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Такая почта уже используется.')
        if UserModel.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Имя пользователя занято.')
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для создания токена аутентификации."""
    username = serializers.CharField()
    confirmation_code = serializers.IntegerField(
        max_value=MAX_CODE, required=True
    )

    def create(self, validated_data):
        username = validated_data['username']
        confirmation_code = validated_data['confirmation_code']
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError(
                'Пользователь с указанным именем не найден'
            )
        cached_code = cache.get(f'confirmation_code_{user.email}')
        if cached_code != str(confirmation_code):
            raise serializers.ValidationError('Неверный код подтверждения')
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""
    class Meta:
        model = UserModel
        fields = [
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message=MESSAGE
        )]
    )

    class Meta:
        model = UserModel
        fields = [
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        ]
