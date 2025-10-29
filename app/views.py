from rest_framework.response import Response
from .models import Room, Message
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from django.core.cache import cache


@api_view(['POST'])
def create_room(request):
    """
    Handles the creation of a chat room.

    This view function processes POST requests to create a new chat room.
    If a room with the specified name does not already exist, it will be created.
    Notes:
        - This function assumes the existence of a Room model with a 'name' field.
    """
    room_name = request.data.get('room_name')  
    if room_name:
        room, created = Room.objects.get_or_create(name=room_name)
        if created:
            return Response({'status': 'Room created'})
        else:
            return Response({'status': 'Room already exists'})
            
    return Response({'status': 'Invalid request', 'error': 'Room name is required'})

@api_view(['GET'])
def get_rooms(request):
    """
    Retrieves a list of all chat rooms.

    This view function processes GET requests to return a list of all existing chat rooms.

    Notes:
        - This function assumes the existence of a Room model with a 'name' field.
    """
    rooms = Room.objects.all().values_list('name', flat=True)
    return Response({'rooms': list(rooms)})

@api_view(['GET'])
def get_messages(request, room_name):
    """
    Retrieves messages for a specific chat room with pagination.
    This view function processes GET requests to return paginated messages associated with a given chat room.
    """
    cache_key = f"room_{room_name}_messages"
    cached_messages = cache.get(cache_key)

    if cached_messages:
        return Response({'messages': cached_messages})
    messages = Message.objects.filter(room__name=room_name).order_by('-timestamp')[:10]
    messages_list = [(message.timestamp, (message.sender), ":" + message.content) for message in messages] # Mini Serializer :)

    cache.set(cache_key, messages_list, timeout=300)  #  5m
    return Response({'messages': messages_list})
