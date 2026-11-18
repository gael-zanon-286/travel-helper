from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.trips.locations.images.models import Image
from api.trips.locations.images.serializers import ImageSerializer
from api.trips.locations.models import Location


@api_view(['GET', 'POST'])
def image(request, trip_id, location_id):
    try:
        location = Location.objects.get(pk=location_id, trip_id=trip_id)
    except Location.DoesNotExist:
        return Response(status=404)
    if request.method == 'GET':
        images = Image.objects.filter(location=location)
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)


    elif request.method == 'POST':
        data = request.data.copy()
        data['location'] = location.pk
        serializer = ImageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

@api_view(['DELETE'])
def image_detail(request, trip_id, location_id, image_id):
    try:
        location = Location.objects.get(pk=location_id, trip_id=trip_id)
    except Location.DoesNotExist:
        return Response(status=404)
    try:
        image = Image.objects.get(pk=image_id, location=location)

        image.delete()
        return Response(status=204)
    except Image.DoesNotExist:
        return Response(status=404)
