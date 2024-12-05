from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from titles.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для категорий.
    """
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор для жанров.
    """
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для GET запросов произведений.
    """
    category = CategorySerializer(
        read_only=True
    )
    genre = GenreSerializer(
        many=True, 
        read_only=True
    )
    rating = serializers.FloatField()

    class Meta:
        model = Title
        fields = '__all__'


class TitlePostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для POST запросов произведений.
    """
    category = serializers.SlugRelatedField(
        slug_field='slug', 
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', 
        queryset=Genre.objects.all(), 
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField()
    title = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'
        validators = (
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['title', 'author'],
            )
        )

    def validate_score(self, value):
        if value['score'] not in range(1, 10):
            raise serializers.ValidationError(
                'Оценка должна быть в пределах от 1 до 10!'
            )
        return value

    def validate(self, value):
        if self.context['request'].method != 'POST':
            return value
        if Review.objects.filter(
            title=self.context['view'].kwargs.get('title_id'),
            author=self.context['request'].user,
        ).exists():
            raise serializers.ValidationError(
                'Отзыв уже написан к произведению!'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = '__all__'
