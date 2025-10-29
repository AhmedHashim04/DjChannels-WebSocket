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
    messages = Message.objects.filter(room__name=room_name).order_by('-created_at')[:10]
    messages_list = [message.content for message in messages]

    cache.set(cache_key, messages_list, timeout=300)  #  5m
    return Response({'messages': messages_list})


@api_view(['POST'])
def send_message(request):
    """
    Handles sending a new message to a chat room.
    This view function processes POST requests to create a new message and updates the cache for the room.
    """
    room_name = request.data.get('room_name')
    content = request.data.get('content')
    if not room_name or not content:
        return Response({'status': 'Invalid request', 'error': 'Room name and content are required'})
    try:
        room = Room.objects.get(name=room_name)
        message = Message.objects.create(room=room, content=content)

        # Update the cache for the room
        cache_key = f"room_{room_name}_messages"
        
        cached_messages = cache.get(cache_key) or []
        cached_messages = [message.content] + cached_messages[:9]  # only last 10 messages
        cache.set(cache_key, cached_messages, timeout=300)
        return Response({'status': 'Message sent'})
    
    except:
        return Response({'status': 'Invalid request', 
                         'error': 'Room does not exist'})