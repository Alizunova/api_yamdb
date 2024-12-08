from django.contrib.auth import get_user_model
from django.db import models

from reviews.сonstants import MAX_LENGTH, SHORT_TEXT_LENGTH


User = get_user_model()


class GenreCategoryModel(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_LENGTH,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Короткая метка',
        unique=True
    )

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class CommentReviewModel(models.Model):
    text = models.TextField(
        verbose_name='Текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:SHORT_TEXT_LENGTH]
