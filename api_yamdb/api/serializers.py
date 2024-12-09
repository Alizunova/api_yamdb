from django.forms import ValidationError
from rest_framework import serializers

from api_yamdb.constants import MAX_SCORE_VALUE, MIN_SCORE_VALUE
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для GET запросов произведений."""

    category = CategorySerializer(
        read_only=True
    )
    genre = GenreSerializer(
        many=True,
        read_only=True
    )
    rating = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Title
        fields = '__all__'


class TitlePostSerializer(serializers.ModelSerializer):
    """Сериализатор для POST запросов произведений."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        allow_empty=False
    )

    class Meta:
        fields = '__all__'
        model = Title

    def to_representation(self, instance):
        """
        Переопределяем метод для корректного вывода данных после
        успешного создания/обновления.
        """
        return TitleSerializer(instance).data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для POST запросов отзывов."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField(
        min_value=MIN_SCORE_VALUE,
        max_value=MAX_SCORE_VALUE,
        error_messages={
            'min_value': f'Оценка не может быть меньше {MIN_SCORE_VALUE}.',
            'max_value': f'Оценка не может быть больше {MAX_SCORE_VALUE}.'
        }
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        if request.method == 'POST' and Review.objects.filter(
            title_id=title_id,
            author=author
        ).exists():
            raise ValidationError('Отзыв уже оставлен.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для POST запросов комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date', 'review')
