from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
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
        verbose_name='Электронная почта',
        max_length=254,
        unique=True
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=CHOICES,
        max_length=10,
        default=USER
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=100,
        editable=False,
        null=True
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator(),]
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
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
                fields=['username', 'email'], 
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username
