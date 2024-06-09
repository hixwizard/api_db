import hashlib
from rest_framework.serializers import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from django.core.validators import RegexValidator

from .mixins import ExtraKwargsMixin
from .models import UserModel
from core.constants import USERNAME_MAX_LENGTH, MAX_CODE, EMAIL_MAX, MESSAGE, CODE_LENGTH


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254)  # Ensure email length is checked
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Имя пользователя должно содержать только буквы, цифры, и символы @/./+/-/_',
        )]
    )

    class Meta:
        model = UserModel
        fields = ('email', 'username')

    def validate(self, data):
        if UserModel.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Такая почта уже используется.')
        if UserModel.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Имя пользователя занято.')
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.IntegerField(max_value=MAX_CODE)

    def create(self, validated_data):
        user = UserModel.objects.get(username=validated_data['username'])
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class UserSerializer(serializers.ModelSerializer, ExtraKwargsMixin):
    """Сериализатор для пользователя."""
    class Meta:
        model = UserModel
        fields = [
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        ]


class UserCreateSerializer(ExtraKwargsMixin, serializers.ModelSerializer):
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
