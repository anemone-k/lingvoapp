# Generated by Django 3.2.3 on 2021-05-29 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lingvoapp', '0014_remove_material_youtubeurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='youtubeUrl',
            field=models.TextField(default='https://www.youtube.com/embed/y3T56egqXLw'),
        ),
    ]