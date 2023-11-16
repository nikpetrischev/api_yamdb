from django.db import models

from .mixins import NameAndSlugAbstract


class Category(NameAndSlugAbstract):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'категории'


class Genre(NameAndSlugAbstract):

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'жанры'


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    year = models.SmallIntegerField()
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        on_delete=models.SET_NULL,
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
    )
    # Костыль
    rating = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'произведения'

    def __str__(self) -> str:
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )
