from django.db import models
from django.contrib.auth import get_user_model

from core.constants import NAME_MAX, SLUG_MAX
User = get_user_model()


class Category(models.Model):
    """Модель категории."""
    name = models.CharField(
        max_length=NAME_MAX,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Slug'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """Модель жанра."""
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
        ordering = ('id',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """Модель произведения."""
    name = models.CharField(
        max_length=NAME_MAX,
        verbose_name='Название',
    )
    year = models.IntegerField(
        verbose_name='Год',
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
        on_delete=models.CASCADE,
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
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Жанр к произведению'
        verbose_name_plural = 'Жанр к произведению'


class Reviews(models.Model):
    """Модель отзыва."""
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='ID произведения'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    score = models.IntegerField(
        verbose_name='Оценка'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self) -> str:
        return self.text


class Comment(models.Model):
    """Модель комментария."""
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='ID произведения'
    )
    review_id = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        verbose_name='ID отзыва',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.text
