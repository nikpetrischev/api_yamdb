# Generated by Django 3.2 on 2023-11-14 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NameAndSlugAbstract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Наименование')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг')),
            ],
        ),
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('nameandslugabstract_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reviews.nameandslugabstract')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'категории',
            },
            bases=('reviews.nameandslugabstract',),
        ),
        migrations.CreateModel(
            name='TitleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('year', models.SmallIntegerField()),
                ('description', models.TextField()),
                ('rating', models.PositiveSmallIntegerField()),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.categorymodel', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'произведения',
            },
        ),
        migrations.CreateModel(
            name='GenreModel',
            fields=[
                ('nameandslugabstract_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reviews.nameandslugabstract')),
                ('title', models.ManyToManyField(related_name='genres', to='reviews.TitleModel', verbose_name='Произведение')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'жанры',
            },
            bases=('reviews.nameandslugabstract',),
        ),
    ]