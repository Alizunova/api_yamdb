from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Жанр"

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name="Название"

    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Произведение"

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1, "Минимальная оценка 1"),
            MaxValueValidator(10, "Максимальная оценка 10"),
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Отзыв"
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name="unique_review"
            )
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Комментарий"

    def __str__(self):
        return self.text[:15]
