# Generated by Django 3.2 on 2023-11-18 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_comment_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='rating',
        ),
    ]
