# Generated by Django 2.1.2 on 2018-11-05 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dosgamesfinder', '0006_remove_dosgame_long_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dosgame',
            old_name='description',
            new_name='long_description',
        ),
    ]