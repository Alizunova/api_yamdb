<div id="header" align="left">
    <img src="https://img.shields.io/badge/Python-blue?logo=python&logoColor=yellow" alt="Python"/>
    <img src="https://img.shields.io/badge/Django-dark_green?logo=django&logoColor=white" alt="Django"/>
    <img src="https://img.shields.io/badge/Django-rest-red?logo=django&logoColor=white" alt="Django Rest"/>
</div>

# Проект YaMDb

## Описание
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 

## Технологии используемые в проекте:
- requests==2.26.0
- Django==3.2
- djangorestframework==3.12.4
- PyJWT==2.1.0
- pytest==6.2.4
- pytest-django==4.4.0
- pytest-pythonpath==0.7.3
- djangorestframework-simplejwt==4.7.2
- django-filter==22.1


## Инструкция по запуску

1) Клонировать репозиторий и перейти в него в командной строке:

```
git clone --single-branch --branch master https://github.com/Alizunova/api_yamdb.git
```

```
cd api_yamdb
```

2) Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/Scripts/activate
```

3) Установить зависимости из файла requirements.txt:

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

4) Выполнить миграции:

```bash
python manage.py migrate
```

5) Создать суперпользователя:

```bash
python manage.py createsuperuser
```

6) Запустить проект:

```bash
python manage.py runserver
```


## Как наполнить БД
Запуск команды загрузки данных из CSV в БД.

```bash
python manage.py upload_data
```

Соответствике моделей с файлами:
- Пользователи <-- users.csv
- Жанры <-- genre.csv
- Категории <-- category.csv
- Произведения и жанры <-- genre_title.csv
- Произведения <-- titles.csv
- Отзывы <-- review.csv
- Комментарии <-- comments.csv


## Авторы

#### Анна Л.
#### Александр С.
#### Александр Р.
