# Generated by Django 3.2.3 on 2021-05-26 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lingvoapp', '0003_auto_20210517_2216'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dictionary',
            options={'ordering': ['id'], 'verbose_name': 'DictionaryWord', 'verbose_name_plural': 'DictionaryWords'},
        ),
        migrations.AlterModelOptions(
            name='dictionaryinverted',
            options={'ordering': ['id'], 'verbose_name': 'DictionaryInvertedWord', 'verbose_name_plural': 'DictionaryInvertedWords'},
        ),
        migrations.AlterModelOptions(
            name='material',
            options={'ordering': ['id'], 'verbose_name': 'Material', 'verbose_name_plural': 'Materials'},
        ),
    ]
