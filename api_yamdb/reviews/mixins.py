from django.db import models


class NameAndSlugAbstract(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование',
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        blank=False,
        null=False,
    )

    def __str__(self) -> str:
        return self.name
