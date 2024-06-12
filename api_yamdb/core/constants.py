NAME_MAX: int = 256
SLUG_MAX: int = 50
USERNAME_MAX_LENGTH: int = 150
MIN_CODE: int = 1000
# type or len
MAX_CODE: int = 99999
# 4 - defaut
CODE_LENGTH: int = 5
EMAIL_MAX: int = 254
POINT_M: int = 2
ROLE_CHOICES: dict = {
    'user': 'user',
    'admin': 'admin',
    'moderator': 'moderator',
}

ROLE_CHOICES_LIST: list = [(key, value) for key, value in ROLE_CHOICES.items()]
MESSAGE: str = 'Имя не должно содержать недопустимых символов.'
