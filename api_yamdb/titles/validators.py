from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_year(value):
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            f'{value} год не корректен.'
        )


validate_slug = RegexValidator(
    regex=r'^[-a-zA-Z0-9_]+$',
    message='Слаг может содержать только буквы, цифры, дефисы и подчёркивания.'
)
