# Generated by Django 4.1.5 on 2024-09-08 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_alter_comment_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='is_bookmarked',
            field=models.BooleanField(default=True),
        ),
    ]
