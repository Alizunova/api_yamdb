from csv import DictReader

from django.conf import settings
from django.db import models


def upload_data(model: models.Model, file: str):
    data_model = []
    with open(settings.UPLOAD_DATA_DIR / file, encoding='utf8') as csvfile:
        for row in DictReader(csvfile):
            data_model.append(model(**row))
    model.objects.bulk_create(data_model)


def modify_data_title(titles: models.Model, genres: models.Model, file: str):
    with open(settings.UPLOAD_DATA_DIR / file, encoding='utf8') as csvfile:
        for row in DictReader(csvfile):
            title = titles.objects.get(id=row['title_id'])
            genre = genres.objects.get(id=row['genre_id'])
            title.genre.add(genre)
