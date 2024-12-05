from django.contrib.auth.models import AbstractUser
from django.db import models

# Дописать кто может заходить в админку


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
        'Электронная почта', max_length=254, unique=True, blank=True)
    role = models.CharField('Роль', choices=CHOICES, max_length=10)
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=100, editable=False, null=True
    )
    username = models.CharField(
        'Имя пользователя', max_length=150, unique=True, blank=True)
    bio = models.CharField(
        verbose_name='Биография',
        max_length=100,
        blank=True,
        null=True
    )

    class Meta(AbstractUser.Meta):

        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username
