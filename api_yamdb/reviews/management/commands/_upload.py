from csv import DictReader
from pathlib import Path

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db import models


def upload_data(file: str, model: models.Model):
    data_model = []
    csv_path = Path(settings.UPLOAD_DATA_DIR) / file
    with open(csv_path, encoding='utf8') as csvfile:
        for row in DictReader(csvfile):
            for field in model._meta.fields:
                if field.is_relation: 
                    related_model = field.related_model
                    field_name = field.name
                    if row.get(field_name):
                        try:
                            row[field_name] = related_model.objects.get(pk=row[field_name])
                        except ObjectDoesNotExist:
                            raise ValueError(
                                f"Ошибка: Не найден объект {related_model.__name__} с id={row[field_name]}"
                            )
            data_model.append(model(**row))
    model.objects.bulk_create(data_model)


def modify_data_title(titles: models.Model, genres: models.Model, file: str):
    csv_path = Path(settings.UPLOAD_DATA_DIR) / file
    with open(csv_path, encoding='utf8') as csvfile:
        for row in DictReader(csvfile):
            title = titles.objects.get(id=row['title_id'])
            genre = genres.objects.get(id=row['genre_id'])
            title.genre.add(genre)
