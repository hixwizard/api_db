from rest_framework.serializers import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import RegexValidator

from .mixins import ExtraKwargsMixin
from .models import UserModel
from core.constants import USERNAME_MAX_LENGTH, MAX_CODE, EMAIL_MAX, MESSAGE


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=EMAIL_MAX)
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message=MESSAGE,
        )]
    )

    class Meta:
        model = UserModel
        fields = ('email', 'username')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError('Имя "me" уже занято.')
        return value

    def validate_email(self, value):
        if len(value) > EMAIL_MAX:
            raise ValidationError(
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
    role = serializers.CharField(read_only=True)

    class Meta:
        model = UserModel
        fields = [
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        ]


class UserCreateSerializer(ExtraKwargsMixin, serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = [
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        ]
