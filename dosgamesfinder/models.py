from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=255, unique=True)        # not used as a primary key, but is unique
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class DosGame(models.Model):
    title = models.CharField(max_length=128)
    genre = models.CharField(max_length=128)
    description = models.TextField()
    date_releated = models.IntegerField()
    user_rating = models.IntegerField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)      # ManyToOne - Publisher can have multiple DosGames, but the DosGame can only have one Publisher

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        
class Screenshot(models.Model):
    game = models.ForeignKey(DosGame, on_delete=models.CASCADE, related_name='screenshots')     # ManyToOne - DosGame can have multiple Screenshots, but the Screenshot can only have one DosGame
    img_src = models.URLField(max_length=255)
    img_width = models.IntegerField()
    img_height = models.IntegerField()

    def __str__(self):
        return self.img_src


class DownloadLocation(models.Model):
    game = models.ForeignKey(DosGame, on_delete=models.CASCADE, related_name='download_locations')     # ManyToOne - DosGame can have multiple DownLoad locations, but the Download Location can only have one DosGame
    href = models.URLField(max_length=255)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)    