from django.contrib import admin
from .models import DosGame, Screenshot, Publisher, DownloadLocation


# Register your models here.
admin.site.register(DosGame)
admin.site.register(Screenshot)
admin.site.register(Publisher)
admin.site.register(DownloadLocation)

