import re
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            f'{value} год не корректен.'
        )


def validate_slug(value):
    pattern = r'^[-a-zA-Z0-9_]+$'
    if not re.match(pattern, value):
        raise ValidationError(
            f'Слаг "{value}" не соответствует требованиям. '
            'Допустимы только буквы, цифры, дефисы и подчёркивания.'
        )
