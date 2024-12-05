from django.contrib.auth.models import AbstractUser
from django.db import models

# Дописать кто может заходить в админку


class MyUser(AbstractUser):
    ANONIMOUS = 'anonimous'
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    SUPERUSER = 'superuser'

    CHOICES = (
        ('anon', ANONIMOUS),
        ('admin', ADMIN),
        ('moderator', MODERATOR),
        ('user', USER),
        ('superuser', SUPERUSER),
    )
    email = models.EmailField('Электронная почта', max_length=25)
    role = models.CharField('Роль', choices=CHOICES, max_length=10)
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=100, editable=False, null=True
    )
    username = models.CharField('Имя пользователя', max_length=30)

    class Meta(AbstractUser.Meta):

        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username
