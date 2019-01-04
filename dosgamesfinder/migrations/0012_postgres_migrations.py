# Manually generated to run postgres migrations for Trigram and Unaccent search

from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension, UnaccentExtension

class Migration(migrations.Migration):

    dependencies = [
        ('dosgamesfinder', '0011_auto_20181118_0026'),
    ]

    operations = [
        TrigramExtension(), 
        UnaccentExtension()
    ]
