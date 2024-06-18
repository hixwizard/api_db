from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.utils.timezone import now

from core.constants import NAME_MAX, SLUG_MAX, SCORE_MAX_VALUE

User = get_user_model()


class BaseModel(models.Model):
    """Абстрактная модель"""
    name = models.CharField(
        max_length=NAME_MAX,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=SLUG_MAX,
        unique=True,
        verbose_name='Slug'
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name


class Category(BaseModel):
    """Модель категории."""

    class Meta:
        ordering = ('id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseModel):
    """Модель жанра."""

    class Meta:
        ordering = ('id',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения."""
    name = models.CharField(
        max_length=NAME_MAX,
        verbose_name='Название',
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год',
        validators=[MaxValueValidator(now().year)]
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='GenreTitle',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name


class GenreTitle(models.Model):
    """Промежуточная модель жанра произведения."""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genres',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='titles',
    )

    class Meta:
        verbose_name = 'Жанр к произведению'
        verbose_name_plural = 'Жанр к произведению'


class Review(models.Model):
    """Модель отзыва."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='ID произведения')
    text = models.TextField(
        verbose_name='Текст отзыва',)
    score = models.PositiveIntegerField(
        validators=[MaxValueValidator(SCORE_MAX_VALUE)],
        verbose_name='Оценка',
    )

    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Время публикации',
        db_index=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review_from_author'
            )
        ]
        ordering = ('id',)

    def __str__(self) -> str:
        return self.text


class Comment(models.Model):
    """Модель комментария."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='ID произведения'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='ID отзыва',
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Время публикации',
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.text
