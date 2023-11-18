# Generated by Django 3.2 on 2023-11-18 10:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_remove_title_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(10, 'Убедитесь, что значение меньше или равно %(limit_value)s.'), django.core.validators.MinValueValidator(1)], verbose_name='Оценка'),
        ),
    ]
