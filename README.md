## Проект YaMDb

YaMDb - API-сервис для публикации отзывов пользователей на различные произведения.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:nnikitagoncharovv/api_yamdb.git
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

```
cd api_yamdb
```

```
Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```
Импортировать данные из CSV-файлов в БД:

```
python manage.py import_data_csv
```

```
Примеры запросов:

Регистрация

POST /api/v1/auth/signup/
body params:
email - required string <= 254 characters
username  - required string <= 150 characters

Получение токена

POST /api/v1/auth/token/
body parameters:
username - required string <= 150 characters 
confirmation_code - required string

Список отзывов на произведение

POST /api/v1/titles/{title_id}/reviews/
path parameters:
    title_id - required integer ID произведения

body parameters:
    text - required string (Текст отзыва)
    score  - required integer (Оценка) [ 1 .. 10 ]

Частичное обновление данных своей учётной записи

PATCH /api/v1/users/me/
body params:

    username - required string <= 150characters Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.

    email  - required string <email> <= 254 characters
    first_name  - string <= 150 characters
    last_name   string <= 150 characters
    bio  - string
```

Используемые технологии:

asgiref==3.6.0
atomicwrites==1.4.1
attrs==23.1.0
certifi==2023.5.7
charset-normalizer==2.0.12
colorama==0.4.6
Django==3.2
django-filter==23.2
djangorestframework==3.12.4
djangorestframework-simplejwt==5.2.2
idna==3.4
iniconfig==2.0.0
packaging==23.1
pluggy==0.13.1
py==1.11.0
PyJWT==2.1.0
pytest==6.2.4
pytest-django==4.4.0
pytest-pythonpath==0.7.3
pytz==2023.3
requests==2.26.0
sqlparse==0.4.4
toml==0.10.2
urllib3==1.26.15

```
Получить доступ к документации:

http://127.0.0.1:8000/redoc/
```

Авторы проекта:
- (https://github.com/nnikitagoncharovv)
- (https://github.com/Lif-a-nova)
- (https://github.com/JewiCat)
