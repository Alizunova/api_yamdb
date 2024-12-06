from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, RegexValidator
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    CHOICES = (
        ('admin', ADMIN),
        ('moderator', MODERATOR),
        ('user', USER),
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True
    )
    role = models.CharField(
        'Роль',
        choices=CHOICES,
        max_length=10,
        default='user'
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        validators=[MaxLengthValidator(254)],
        max_length=100,
        editable=False,
        null=True
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]',
                message='Недопустимые символы в имени пользователя.'
            )
        ]
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    class Meta(AbstractUser.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username
