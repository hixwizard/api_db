from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import RegexValidator

from .mixins import ExtraKwargsMixin
from users.models import UserModel
from core.constants import USERNAME_MAX_LENGTH, MAX_CODE, EMAIL_MAX, MESSAGE
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
    rating = serializers.IntegerField(read_only=True,)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def validate_year(self, value):
        if value > now().year:
            serializers.ValidationError(
                'Год выпуска не может быть больше текущего')
        return value


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


class TitleGetSerializer(TitleSerializer):
    """Сериализатор получения произведений."""
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)


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
            title_id = self.context.get('view').kwargs.get('title_id')
            title = get_object_or_404(Title, pk=title_id)
            if Review.objects.filter(author=author, title_id=title).exists():
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


class SignupSerializer(serializers.ModelSerializer):
    '''Сериализатор регистриции.'''
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
