NAME_MAX = 256
SLUG_MAX = 50
USERNAME_MAX_LENGTH = 150
MIN_CODE = 1000
MAX_CODE = 9999
CODE_LENGTH = 4
EMAIL_MAX = 254

ROLE_CHOICES = {
    'user': 'user',
    'admin': 'admin',
    'moderator': 'moderator',
}

ROLE_CHOICES_LIST = [(key, value) for key, value in ROLE_CHOICES.items()]
