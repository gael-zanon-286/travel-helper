from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.trips.locations.models import Location
from api.trips.locations.serializers import LocationSerializer
from api.trips.models import Trip


@api_view(['GET', 'POST'])
def location(request, trip_id):
    try:
        trip = Trip.objects.get(pk=trip_id)
    except Trip.DoesNotExist:
        return Response(status=404)
    if request.method == 'GET':
        trips = Location.objects.filter(trip_id=trip_id)
        serializer = LocationSerializer(trips, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(trip=trip)
        return Response(serializer.data, status=201)

@api_view(['GET', 'PUT', 'DELETE'])
def location_detail(request, trip_id, location_id):
    try:
        location = Location.objects.get(pk=location_id, trip_id=trip_id)
    except Location.DoesNotExist:
        return Response(status=404)

    if request.method == "GET":
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = LocationSerializer(location, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == "DELETE":
        location.delete()
        return Response(status=204)