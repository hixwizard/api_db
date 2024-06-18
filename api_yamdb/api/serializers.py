import random
from django.core.mail import send_mail
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import RegexValidator
from django.core.cache import cache

from .mixins import ExtraKwargsMixin
from users.models import UserModel
from core.constants import (USERNAME_MAX_LENGTH, MAX_CODE, EMAIL_MAX, MESSAGE,
                            MIN_CODE, MAX_CODE, FIVE_MIN, ADMIN_EMAIL)
from reviews.models import Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Общий сериализатор произведений."""

    class Meta:
        model = Title
        fields = '__all__'


class TitlePostSerializer(TitleSerializer):
    """Сериализатор добавления и изменения произведений."""
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    def validate_year(self, value):
        if value > now().year:
            serializers.ValidationError(
                'Год выпуска не может быть больше текущего')
        return value


class TitleGetSerializer(TitleSerializer):
    """Сериализатор получения произведений."""
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)


class ReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    def validate(self, attrs):
        request = self.context.get('request')
        if request.method == 'POST':
            author = request.user
            if Review.objects.filter(
                author=author,
                title_id=self.context.get('view').kwargs.get('title_id')
            ).exists():
                raise serializers.ValidationError(
                    'Нельзя создать повторный отзыв на это произведение')
        return attrs

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)


class SignupSerializer(serializers.Serializer):
    """Сериализатор регистрации."""
    email = serializers.EmailField(max_length=EMAIL_MAX)
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message=MESSAGE,
        )]
    )

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        if username.lower() == 'me':
            raise serializers.ValidationError('Имя "me" уже занято.')
        if len(email) > EMAIL_MAX:
            raise serializers.ValidationError(
                'Email не может быть длиннее 254 символов.')
        email_exists = UserModel.objects.filter(email=email).exists()
        username_exists = UserModel.objects.filter(username=username).exists()
        if email_exists and not username_exists:
            raise serializers.ValidationError(
                'Такая почта уже используется, но имя пользователя свободно.')
        if email_exists:
            raise serializers.ValidationError('Такая почта уже используется.')
        if username_exists:
            raise serializers.ValidationError('Имя пользователя занято.')
        return data

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        confirmation_code = str(random.randint(MIN_CODE, MAX_CODE))
        user, created = UserModel.objects.get_or_create(
            username=username,
            defaults={'email': email})
        if not created and user.email != email:
            raise serializers.ValidationError('Такая почта уже используется.')
        user.confirmation_code = confirmation_code
        user.save()
        cache_key = f'confirmation_code_{username}'
        cache.set(cache_key, confirmation_code, timeout=FIVE_MIN)
        send_mail(
            'Код подтверждения для входа.',
            f'Ваш код подтверждения {confirmation_code}',
            ADMIN_EMAIL,
            [email],
            fail_silently=False,)
        return user, created


class TokenSerializer(serializers.Serializer):
    """Сериализатор токена."""
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
    """Сериализатор для создания пользователей."""
    class Meta:
        model = UserModel
        fields = [
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        ]
