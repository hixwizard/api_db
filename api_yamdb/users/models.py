from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from core.constants import (
    USERNAME_MAX_LENGTH, EMAIL_MAX, ROLE_CHOICES,
    ROLE_CHOICES_LIST, MAX_ROLE_LENGTH
)


class UserModel(AbstractUser):
    """Кастомная модель пользователя."""
    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='Разрешены только буквы, цифры и символы @ . + - _',)]
    )
    email = models.EmailField(max_length=EMAIL_MAX, unique=True)
    first_name = models.CharField(max_length=USERNAME_MAX_LENGTH, blank=True)
    last_name = models.CharField(max_length=USERNAME_MAX_LENGTH, blank=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'роль',
        max_length=MAX_ROLE_LENGTH,
        choices=ROLE_CHOICES_LIST,
        default=ROLE_CHOICES['user'],
        blank=True
    )

    @property
    def is_admin(self):
        return self.role == ROLE_CHOICES['admin']

    @property
    def is_moderator(self):
        return self.role == ROLE_CHOICES['moderator']

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username
