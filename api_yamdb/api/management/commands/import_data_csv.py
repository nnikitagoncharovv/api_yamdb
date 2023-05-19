import csv
import os
from pathlib import Path

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
from api_yamdb.settings import BASE_DIR
from users.models import User

MODELS_CSV = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    TitleGenre: 'genre_title.csv',
}

fields_to_replace = {
    MODELS_CSV[Title]: ('category_id', 'category'),
    MODELS_CSV[Review]: ('author_id', 'author'),
    MODELS_CSV[Comment]: ('author_id', 'author'),
}

path_to_csv_directory = os.path.join(BASE_DIR, 'static/', 'data/')


class Command(BaseCommand):
    """Импорт данных из CSV в БД"""

    def handle(self, *arg, **options):
        def __init__(self, *arg, **kwargs):
            super().__init__(*arg, **kwargs)

        def import_csv(model, csv_file, csv_file_path):
            with open(csv_file_path, 'r', encoding='utf-8') as data_csv_file:
                reader = csv.DictReader(data_csv_file)
                if csv_file in fields_to_replace:
                    for row in reader:
                        db_fields, scv_fields = fields_to_replace[csv_file]
                        row[db_fields] = row.pop(scv_fields)
                        model.objects.create(**row)
                else:
                    for row in reader:
                        model.objects.create(**row)
                self.stdout.write(
                    self.style.SUCCESS(
                    f'Данные из файла {csv_file} импортированы'
                    f'в БД {model.__name__}.'
                    )
                )
        
        for model, csv_file in MODELS_CSV.items():
            csv_file_path = Path(path_to_csv_directory) / csv_file
            import_csv(model, csv_file, csv_file_path)
