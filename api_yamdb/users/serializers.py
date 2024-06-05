from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserModel
from core.constants import USERNAME_MAX_LENGTH, CODE_LENGTH


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=USERNAME_MAX_LENGTH)

    def validate(self, data):
        if UserModel.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Такая почта уже изпользуется.')
        if UserModel.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Имя пользователя занято.')
        return data


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=USERNAME_MAX_LENGTH)
    confifmation_code = serializers.CharField(max_length=CODE_LENGTH)

    def validate(self, data):
        user = UserModel.objects.filter(
            username=data['username'],
            confirmation_code=data['confirmation_code']).first()
        if not user:
            raise serializers.ValidationError(
                'Неверное имя пользователя или код подтвержения'
            )
        return data

    def create(self, validated_data):
        user = UserModel.objects.get(
            username=validated_data['username']
        )
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
