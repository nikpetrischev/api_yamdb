# Django Library
from django.db import models


class NameAndSlugAbstract(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование',
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        max_length=50,
    )

    def __str__(self) -> str:
        return self.slug
