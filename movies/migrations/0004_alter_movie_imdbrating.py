# Generated by Django 4.1.5 on 2024-09-04 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_alter_movie_imdbrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='imdbrating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
