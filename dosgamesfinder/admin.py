from django.contrib import admin
from .models import DosGame, Genre, Screenshot, Publisher, DownloadLocation

# Register your models here.
admin.site.register(DosGame)
admin.site.register(Genre)
admin.site.register(Publisher)
admin.site.register(Screenshot)
admin.site.register(DownloadLocation)

