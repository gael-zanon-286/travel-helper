from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.trips.models import Trip
from api.trips.serializers import TripSerializer

@api_view(['GET', 'POST'])
def trip(request):
    if request.method == 'GET':
        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TripSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

@api_view(['GET', 'PUT', 'DELETE'])
def trip_detail(request, trip_id):
    try:
        trip = Trip.objects.get(pk=trip_id)
    except Trip.DoesNotExist:
        return Response(status=404)

    if request.method == "GET":
        serializer = TripSerializer(trip)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = TripSerializer(trip, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == "DELETE":
        trip.delete()
        return Response(status=204)