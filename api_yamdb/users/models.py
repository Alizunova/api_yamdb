import users.constants as con
from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import validate_username
from django.contrib.auth.validators import UnicodeUsernameValidator

class User(AbstractUser):

    CHOICES = (
        ("admin", con.ADMIN),
        ("moderator", con.MODERATOR),
        ("user", con.USER),
    )

    email = models.EmailField(
        verbose_name="Электронная почта",
        max_length=con.EMAIL_MAX_LENGHT,
        unique=True
    )
    role = models.CharField(
        verbose_name="Роль",
        choices=CHOICES,
        max_length=con.ROLE_MAX_LENGHT,
        default=con.USER,
    )
    username = models.CharField(
        verbose_name="Имя пользователя",
        max_length=con.USERNAME_MAX_LENGHT,
        unique=True,
        validators=[UnicodeUsernameValidator(), validate_username]
        #validators=[validate_username, validate_slug],
    )
    bio = models.TextField(
        verbose_name="Биография",
        blank=True,
    )

    @property
    def is_admin(self):
        return self.role == con.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == con.MODERATOR

    class Meta(AbstractUser.Meta):
        ordering = ["username"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        constraints = [
            models.UniqueConstraint(
                fields=["username", "email"], name="unique_username_email"
            )
        ]

    def __str__(self):
        return self.username
