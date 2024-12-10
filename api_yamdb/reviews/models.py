from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb.constants import (
    MAX_TEXT_LENGTH,
    MAX_SCORE_VALUE,
    MIN_SCORE_VALUE,
    SHORT_TEXT_LENGTH
)
from reviews.validators import validate_year


User = get_user_model()


class GenreCategoryModel(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_TEXT_LENGTH,
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


class Category(GenreCategoryModel):

    class Meta(GenreCategoryModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(GenreCategoryModel):

    class Meta(GenreCategoryModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_TEXT_LENGTH
    )
    year = models.SmallIntegerField(
        verbose_name='Год выпуска',
        validators=[validate_year]
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='TitleGenre'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['category', 'name']
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genre',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение - Жанр'
        verbose_name_plural = 'Произведения - Жанры'

    def __str__(self):
        return f'{self.title.name} - {self.genre.name}'


class Review(CommentReviewModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(
                MIN_SCORE_VALUE,
                f'Минимальная оценка {MIN_SCORE_VALUE}'
            ),
            MaxValueValidator(
                MAX_SCORE_VALUE,
                f'Максимальная оценка {MAX_SCORE_VALUE}'
            ),
        ]
    )

    class Meta(CommentReviewModel.Meta):
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review'
            )
        ]


class Comment(CommentReviewModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )

    class Meta(CommentReviewModel.Meta):
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
