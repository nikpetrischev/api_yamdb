from typing import Any, Union, TypeVar
import csv
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from api_yamdb.settings import CSV_FILES_DIR
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
    TitleGenre
)


user = get_user_model()


class Command(BaseCommand):
    help = 'Импортирует данные из .csv'
    requires_migrations_check = True

    @transaction.atomic
    def basic_import(self, csv_file: str, model: TypeVar('Model')) -> None:
        # Импорт из .csv в модели, без внешних ключей.
        with open(csv_file) as file:
            csvreader = csv.reader(file)
            keys: list[str] = list()

            for row in csvreader:
                if not keys:
                    keys = row
                    continue

                model_dict = {keys[i]: row[i] for i in range(len(keys))}
                model(**model_dict).save()

    @transaction.atomic
    def complex_import(
        self,
        csv_file: str,
        model: TypeVar('Model'),
        models_for_foreign_keys: dict[str, TypeVar('Model')],
    ) -> None:
        with open(csv_file) as file:
            csvreader = csv.reader(file)
            model_dict: dict[str, Any] = dict()
            keys: list[str] = list()

            for row in csvreader:
                if not keys:
                    keys = row
                    continue

                for i in range(len(keys)):
                    if keys[i] not in models_for_foreign_keys.keys():
                        model_dict[keys[i]] = row[i]
                    else:
                        foreign_key = (models_for_foreign_keys.get(keys[i])
                                       .objects.get(pk=int(row[i])))
                        model_dict[keys[i]] = foreign_key

                model(**model_dict).save()

    def handle(self, *args: Any, **options: Any) -> Union[str, None]:
        self.basic_import(
            os.path.join(CSV_FILES_DIR, 'category.csv'),
            Category,
        )
        self.basic_import(
            os.path.join(CSV_FILES_DIR, 'genre.csv'),
            Genre,
        )
        self.basic_import(
            os.path.join(CSV_FILES_DIR, 'users.csv'),
            user,
        )

        self.complex_import(
            os.path.join(CSV_FILES_DIR, 'titles.csv'),
            Title,
            {'category': Category},
        )
        self.complex_import(
            os.path.join(CSV_FILES_DIR, 'genre_title.csv'),
            TitleGenre,
            {'title_id': Title, 'genre_id': Genre},
        )
        self.complex_import(
            os.path.join(CSV_FILES_DIR, 'review.csv'),
            Review,
            {'title_id': Title, 'author': user},
        )
        self.complex_import(
            os.path.join(CSV_FILES_DIR, 'comments.csv'),
            Comment,
            {'review_id': Review, 'author': user},
        )
