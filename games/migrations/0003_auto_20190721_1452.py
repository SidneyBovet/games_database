# Generated by Django 2.2.3 on 2019-07-21 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20190721_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='own_date',
            field=models.DateField(verbose_name='date published'),
        ),
    ]
