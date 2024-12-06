from csv import DictReader
from pathlib import Path

from django.conf import settings
from django.db import models


def upload_data(file: str, model: models.Model):
    csv_path = Path(settings.UPLOAD_DATA_DIR) / file
    with open(csv_path, encoding='utf8') as csvfile:
        for row in DictReader(csvfile):
            for field in model._meta.fields:
                if field.is_relation: 
                    related_model = field.related_model
                    field_name = field.name
                    pass # активно идет работа


def modify_data_title(titles: models.Model, genres: models.Model, file: str):
    csv_path = Path(settings.UPLOAD_DATA_DIR) / file
    with open(csv_path, encoding='utf8') as csvfile:
        for row in DictReader(csvfile):
            title = titles.objects.get(id=row['title_id'])
            genre = genres.objects.get(id=row['genre_id'])
            title.genre.add(genre)
