# Generated by Django 3.2.3 on 2021-05-29 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lingvoapp', '0016_alter_material_youtubeurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='youtubeUrl',
            field=models.TextField(blank=True, default=''),
        ),
    ]
