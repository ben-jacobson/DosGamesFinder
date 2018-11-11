from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify

class Publisher(models.Model):
    slug = models.SlugField(unique=True, max_length=255)    
    name = models.CharField(unique=True, max_length=255, blank=False)     
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Publisher, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('PublisherDetailView', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class Genre(models.Model):
    slug = models.SlugField(unique=True, max_length=255)    
    name = models.CharField(unique=True, max_length=255, blank=False)        

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Genre, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('GenreDetailView', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)        

class DosGame(models.Model):
    slug = models.SlugField(unique=True, max_length=128)    
    title = models.CharField(max_length=128, blank=False)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)      # ManyToOne - Genre can have multiple DosGames, but the DosGame can only have one Genre
    
    long_description = models.TextField(blank=True)         
    short_description = models.CharField(max_length=256, blank=True)

    year_released = models.PositiveIntegerField()
    user_rating = models.PositiveIntegerField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)      # ManyToOne - Publisher can have multiple DosGames, but the DosGame can only have one Publisher
    thumbnail_src = models.URLField(max_length=255)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.create_short_description()
        super(DosGame, self).save(*args, **kwargs)

    def create_short_description(self):
        '''
        In creating new DosGame objects, we create our long descriptions and this function will truncate to automatically create a short_description
        '''
        if len(self.long_description) <= 256:       # copy long to short if the length is right
            self.short_description = self.long_description
        else:
            truncated_string = self.long_description[:(255 - 3)]
            truncated_string += '...'
            self.short_description = truncated_string

    def get_absolute_url(self):
        return reverse('DosGamesDetailView', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        
class Screenshot(models.Model):
    game = models.ForeignKey(DosGame, on_delete=models.CASCADE, related_name='screenshots')     # ManyToOne - DosGame can have multiple Screenshots, but the Screenshot can only have one DosGame
    img_src = models.URLField(max_length=255)
    img_width = models.PositiveIntegerField()
    img_height = models.PositiveIntegerField()

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