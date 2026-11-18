from django.db import models

from api import trips

class Image(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='trip_images/')

    location = models.ForeignKey(
        'trips.Location',
        on_delete=models.CASCADE,
        related_name='images'
    )