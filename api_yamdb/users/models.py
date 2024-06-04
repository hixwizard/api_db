from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from core.constants import USERNAME_MAX_LENGTH, EMAIL_MAX


class UserModel(AbstractBaseUser):
    """Кастомная модель пользователя."""
    username = models.CharField(max_length=USERNAME_MAX_LENGTH, unique=True)
    email = models.EmailField(max_length=EMAIL_MAX)
    first_name = models.CharField(max_length=USERNAME_MAX_LENGTH)
    last_name = models.CharField(max_length=USERNAME_MAX_LENGTH)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(default='user')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username
