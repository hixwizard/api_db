from django.contrib.auth.models import AbstractUser
from django.db import models

from core.constants import (
    USERNAME_MAX_LENGTH, EMAIL_MAX,
    ROLE_CHOICES, USER, ROLE_CHOICES_LIST
)


class UserModel(AbstractUser):
    """Кастомная модель пользователя."""
    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH, unique=True
    )
    email = models.EmailField(max_length=EMAIL_MAX)
    first_name = models.CharField(max_length=USERNAME_MAX_LENGTH)
    last_name = models.CharField(max_length=USERNAME_MAX_LENGTH)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'роль',
        max_length=20,
        choices=ROLE_CHOICES_LIST,
        default=USER,
        blank=True
    )

    @property
    def is_admin(self):
        return self.role == ROLE_CHOICES['admin']

    @property
    def is_moderator(self):
        return self.role == ROLE_CHOICES['moderator']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username
