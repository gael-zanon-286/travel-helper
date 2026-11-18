from django.db import models
from .locations.models import Location
from .locations.images.models import Image

class Trip(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

