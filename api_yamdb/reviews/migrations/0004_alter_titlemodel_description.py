# Generated by Django 3.2 on 2023-11-16 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_alter_titlemodel_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titlemodel',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
    ]
