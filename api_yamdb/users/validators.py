import users.constants as con
from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() in con.ME:
        raise ValidationError('Нельзя создать юзера с ником me.')
