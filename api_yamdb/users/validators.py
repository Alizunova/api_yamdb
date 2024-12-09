from django.core.exceptions import ValidationError

from users.constants import BAD_USERNAME


def validate_username(value):
    if value.lower() in BAD_USERNAME:
        raise ValidationError(
            f'Нельзя создать пользователя с username={value}.'
        )
