from rest_framework import serializers

from api.trips.models import Trip

class TripSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields = ['id', 'name', 'start_date', 'end_date']