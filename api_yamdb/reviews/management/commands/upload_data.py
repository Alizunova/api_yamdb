from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from reviews.management.commands._upload import upload_data, modify_data_title
from reviews.models import Category, Comment, Genre, Review, Title


User = get_user_model()


FILE_MODEL = {
    'users.csv': User,
    'category.csv': Category,
    'genre.csv': Genre,
    'titles.csv': Title,
    'review.csv': Review,
    'comments.csv': Comment,
}


class Command(BaseCommand):
    help = 'Загружает данные из CSV файлов в базу данных'

    def handle(self, *args, **options):
        for file, model in FILE_MODEL.items():
            name = model.__name__
            self.stdout.write(f'Загрузка данных из {file} в модель {name}...')
            upload_data(file, model)
        self.stdout.write('Установка связей между произведениями и жанрами...')
        modify_data_title(Title, Genre, 'genre_title.csv')
        self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))
