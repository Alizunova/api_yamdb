from csv import DictReader
from pathlib import Path

from django.conf import settings
from django.db import models


def upload_data(file: str, model: models.Model):
    data_model = []
    csv_path = Path(settings.UPLOAD_DATA_DIR) / file
    with open(csv_path, encoding='utf8') as csvfile:
        for row in DictReader(csvfile):
            for field in model._meta.fields:
                if not field.is_relation:
                    continue
                related_model = field.related_model
                field_name = field.name
                if not row.get(field_name):
                    continue
                if obj := related_model.objects.get(pk=row[field_name]):
                    row[field_name] = obj
            data_model.append(model(**row))
    model.objects.bulk_create(data_model)


def modify_data_title(titles: models.Model, genres: models.Model, file: str):
    csv_path = Path(settings.UPLOAD_DATA_DIR) / file
    with open(csv_path, encoding='utf8') as csvfile:
        for row in DictReader(csvfile):
            title = titles.objects.get(id=row['title_id'])
            genre = genres.objects.get(id=row['genre_id'])
            title.genre.add(genre)
