# Generated by Django 2.2.16 on 2022-04-03 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]