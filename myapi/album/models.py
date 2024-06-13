from django.db import models

# Create your models here.
class Album(models.Model):
    album_name = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)

    def __str__(self):
        return self.album_name
    
class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    order = models.IntegerField()
    title = models.CharField(max_length=100)
    duration = models.IntegerField()

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return "%d: %s" % (self.order, self.title)