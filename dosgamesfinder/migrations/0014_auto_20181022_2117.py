# Generated by Django 2.1.2 on 2018-10-22 21:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dosgamesfinder', '0013_publisher_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dosgame',
            old_name='date_releated',
            new_name='year_released',
        ),
    ]