# Generated by Django 3.2 on 2023-11-26 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='bio',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]