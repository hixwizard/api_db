from core.constants import USERNAME_MAX_LENGTH, EMAIL_MAX


class ExtraKwargsMixin:
    """Миксин валидации пользователей."""
    class Meta:
        extra_kwargs = {
            'username': {'max_length': USERNAME_MAX_LENGTH},
            'email': {'max_length': EMAIL_MAX, 'validators': []},
            'first_name': {'max_length': USERNAME_MAX_LENGTH},
            'last_name': {'max_length': USERNAME_MAX_LENGTH},
            'bio': {'allow_blank': True},
            'role': {'allow_blank': True},
        }
