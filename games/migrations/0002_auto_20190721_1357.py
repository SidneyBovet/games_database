# Generated by Django 2.2.3 on 2019-07-21 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genre',
            old_name='genre_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='type',
            old_name='type_name',
            new_name='name',
        ),
    ]
