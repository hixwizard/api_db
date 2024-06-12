from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
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
    """
    список(title), 200, 404
    объект индекса(title, review), 200 obj id
    post(jwt, text, score), auth
    !patch(admin or owner),
    !delete(admin or owner)
    """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='title'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    score = models.PositiveIntegerField(
        validators=[MaxValueValidator(10),],
        verbose_name='score',
    )
    author = models.ForeignKey(
        User,
        verbose_name='author',
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField()

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self) -> str:
        return self.text


class Comment(models.Model):
    """
    get 200, 404 list allow any
    get obj com-rev
    post pk-rev
    !patch admin or owner
    !delete admin or owner
    """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='title'
    )
    review = models.ForeignKey( # ?
        Review,
        on_delete=models.CASCADE,
        verbose_name='review',
    )
    text = models.TextField(
        verbose_name='comment text',
    )
    author = models.ForeignKey(
        User,
        verbose_name='author',
        on_delete=models.CASCADE
    )
    crated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.text
