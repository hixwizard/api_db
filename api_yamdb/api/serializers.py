from django.utils.timezone import now
from rest_framework import serializers

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
    '''Сериализатор связаной модели.'''
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
    '''Сериализатор связаной модели.'''
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""
    author = serializers.StringRelatedField(
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('title', 'author', 'text', 'score')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""

    class Meta:
        model = Comment
        fields = ('text',)
