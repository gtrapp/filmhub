# Generated by Django 5.0.3 on 2024-08-30 05:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_remove_movie_watchlist_movie_mylist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='mylist',
            field=models.ManyToManyField(blank=True, related_name='movie_mylist', to=settings.AUTH_USER_MODEL),
        ),
    ]
