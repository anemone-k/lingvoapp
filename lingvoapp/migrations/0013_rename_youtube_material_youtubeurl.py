# Generated by Django 3.2.3 on 2021-05-29 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lingvoapp', '0012_alter_material_youtube'),
    ]

    operations = [
        migrations.RenameField(
            model_name='material',
            old_name='youtube',
            new_name='youtubeUrl',
        ),
    ]