from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            f'{value} год не корректен.'
            f'Введите корректный год'
        )


validate_slug = RegexValidator(
    r'^[-a-zA-Z0-9_]+$',
    'Можно использовать латинские символы, цифры, дефисы и подчёркивания.'
)
