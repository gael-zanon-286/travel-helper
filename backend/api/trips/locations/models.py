from django.db import models

from api import trips

class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    trip = models.ForeignKey(
        'trips.Trip',
        on_delete=models.CASCADE,
        related_name='locations'
    )
    #start_date = models.DateTimeField()
    #end_date = models.DateTimeField()

