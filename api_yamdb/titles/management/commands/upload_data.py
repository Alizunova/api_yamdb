from django.core.management import BaseCommand

from titles.management.commands._upload import upload_data, modify_data_title
from titles.models import Category, Comment, Genre, Review, Title, User

FILE_MODEL = {
    'category.csv': Category,
    'comments.csv': Comment,
    'genre.csv': Genre,
    'review.csv': Review,
    'titles.csv': Title,
    'users.csv': User
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        for file, model in FILE_MODEL.items():
            upload_data(file, model)
            if model is Title:
                modify_data_title(Title, Genre, 'genre_title.csv')
