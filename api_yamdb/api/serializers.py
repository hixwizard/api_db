from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework import serializers, status, validators
from rest_framework.response import Response

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
    """Сериализатор названий."""
    rating = serializers.IntegerField(read_only=True, required=False)

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
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)


class ReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов"""
    author = serializers.StringRelatedField(read_only=True)
    id = serializers.PrimaryKeyRelatedField(read_only=True)

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
        fields = (
            'id',
            'author',
            'text',
            'score',
            'pub_date'
        )


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    def validate(self, attrs):
        if self.context.get('request').method == 'PUT':
            return Response(
                data="PUT запрос не предусмотрен",
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return attrs

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        read_only_fields = (
            'author',
            'post',
        )
