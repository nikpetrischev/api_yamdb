import csv
import os
from typing import Any, Union, TypeVar

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
)


user = get_user_model()

IMPORT_PARAMS_TUPLE: tuple[
    tuple[
        str,
        TypeVar('Model'),
        dict[str, TypeVar('Model')],
    ],
] = (
    (os.path.join(CSV_FILES_DIR, 'category.csv'), Category, {}),
    (os.path.join(CSV_FILES_DIR, 'genre.csv'), Genre, {}),
    (os.path.join(CSV_FILES_DIR, 'users.csv'), user, {}),
    (os.path.join(CSV_FILES_DIR, 'titles.csv'), Title, {'category': Category}),
    (os.path.join(CSV_FILES_DIR, 'genre_title.csv'), Title.genre.through, {}),
    (os.path.join(CSV_FILES_DIR, 'review.csv'), Review, {'author': user}),
    (os.path.join(CSV_FILES_DIR, 'comments.csv'), Comment, {'author': user}),
)


class Command(BaseCommand):
    help = 'Импортирует данные из .csv'
    requires_migrations_check = True

    @transaction.atomic
    def csv_import(
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
        for (csv_path, model,
             model_related_fields) in IMPORT_PARAMS_TUPLE:
            self.csv_import(csv_path, model, model_related_fields)
