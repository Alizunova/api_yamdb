from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from users.constants import (
    ADMIN,
    CHOICES,
    EMAIL_MAX_LENGHT,
    MODERATOR,
    USER,
    USERNAME_MAX_LENGHT
)
from users.validators import validate_username


class User(AbstractUser):

    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=EMAIL_MAX_LENGHT,
        unique=True
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=CHOICES,
        max_length=max([len(field) for field, _ in CHOICES]),
        default=USER,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=USERNAME_MAX_LENGHT,
        unique=True,
        validators=[UnicodeUsernameValidator(), validate_username]
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )

    class Meta(AbstractUser.Meta):
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR
