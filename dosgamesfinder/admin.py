from django.contrib import admin
from .models import DosGame, Genre, Publisher, Screenshot, DownloadLocation

class ScreenshotInline(admin.TabularInline):
    model = Screenshot

class DownloadLocationInline(admin.TabularInline):
    model = DownloadLocation

@admin.register(DosGame)
class DosGameAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'genre', 'publisher', 'year_released', 'user_rating')
    fields = ('slug', 'title', 'genre', 'long_description', 'year_released', 'user_rating', 'publisher', 'thumbnail_src')
    list_filter = ('genre', 'publisher')

    inlines = [
        ScreenshotInline,
        DownloadLocationInline,
    ]

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'games_in_this_genre')

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'games_by_this_publisher')