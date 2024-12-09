from django.contrib import admin

from api_yamdb.constants import EMPTY_VALUE
from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre


admin.site.empty_value_display = EMPTY_VALUE


class GenreInTabular(admin.TabularInline):
    model = TitleGenre
    extra = 1


@admin.register(Category)
@admin.register(Genre)
class GenreCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['review', 'text', 'author', 'pub_date']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'score', 'text', 'author', 'pub_date']


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'get_genre', 'category', 'description']
    list_editable = ('category',)
    fields = ['name', 'year', 'category', 'description']
    inlines = [GenreInTabular]

    @admin.display(description='Жанр')
    def get_genre(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()])
