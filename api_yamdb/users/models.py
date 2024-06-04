from django.contrib.auth.models import AbstractUser
from django.db import models

from core.constants import CODE_LENGTH


class UserModel(AbstractUser):
    """Кастомная модель пользователя."""
    confirmation_code = models.CharField(
        max_length=CODE_LENGTH, blank=True, null=True
    )
