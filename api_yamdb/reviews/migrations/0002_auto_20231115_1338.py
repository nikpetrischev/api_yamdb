# Generated by Django 3.2 on 2023-11-15 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genremodel',
            name='title',
        ),
        migrations.CreateModel(
            name='TitleGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.genremodel')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.titlemodel')),
            ],
        ),
        migrations.AddField(
            model_name='titlemodel',
            name='genre',
            field=models.ManyToManyField(through='reviews.TitleGenre', to='reviews.GenreModel'),
        ),
    ]
