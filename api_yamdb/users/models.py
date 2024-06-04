from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):
    """Кастомная модель пользователя."""
    bio = models.TextField('Биография', blank=True)
