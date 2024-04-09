from django.http import JsonResponse
from base.models import Room
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RoomSerializer
from base.api import serializers


@api_view(['GET'])   #allow only get request
def getRoutes(request):
  routes = [
    'GET /api',
    'GET /api/rooms',  #api to ppl to see room of our application
    # so this would give Json array of objects of all the rooms of our app
    'GET /api/rooms/:id'   # this would give information about a single room 

  ]
  return Response(routes)
  # return JsonResponse(routes, safe=False)
  # safe=false means we can use more than python dictionary in the response


@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True) #many=true are there multiple serializers we need to serialize or one
    return Response(serializer.data)


@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)  #return single object therefore false
    return Response(serializer.data)