# Generated by Django 3.2.3 on 2021-05-29 21:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lingvoapp', '0017_alter_material_youtubeurl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material',
            name='youtubeUrl',
        ),
    ]
