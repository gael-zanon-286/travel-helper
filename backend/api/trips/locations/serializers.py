from rest_framework import serializers

from api.trips.locations.models import Location

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ['id', 'name', 'description', 'latitude', 'longitude']