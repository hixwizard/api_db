from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserModel
from core.constants import USERNAME_MAX_LENGTH, MAX_CODE


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации новых пользователей."""
    email = serializers.EmailField()
    username = serializers.CharField(max_length=USERNAME_MAX_LENGTH)

    class Meta:
        model = UserModel
        fields = ('email', 'username')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Имя "me" уже занято.')

    def validate(self, data):
        if UserModel.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Такая почта уже изпользуется.')
        if UserModel.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Имя пользователя занято.')
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для создания токена аутентификации."""
    email = serializers.EmailField()
    confirmation_code = serializers.IntegerField(max_value=MAX_CODE)

    def create(self, validated_data):
        user = UserModel.objects.get(email=validated_data['email'])
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
    """Сериализатор для создания пользователя."""
    class Meta:
        model = UserModel
        fields = [
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        ]
