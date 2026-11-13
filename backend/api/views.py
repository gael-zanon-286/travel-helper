from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import ModelSerializer


@api_view(['GET'])
def api_get(request):
    return Response({
        'status': 'ok',
        'message': 'API test is working'
    })

@api_view(['POST'])
def api_post(request):
    serializer = ModelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)