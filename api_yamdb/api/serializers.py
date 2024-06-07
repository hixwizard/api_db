from django.utils.timezone import now
from rest_framework import serializers

from reviews.models import Category, Genre, Title, Reviews, Comment


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

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        if value > now().year:
            serializers.ValidationError(
                'Год выпуска не может быть больше текущего')
        return value


class ReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""

    class Meta:
        model = Reviews
        fields = ('text', 'score')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""

    class Meta:
        model = Comment
        fields = ('text')
