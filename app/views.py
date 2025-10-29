from rest_framework.response import Response
from .models import Room, Message


def create_room(request):
    """
    Handles the creation of a chat room.

    This view function processes POST requests to create a new chat room.
    If a room with the specified name does not already exist, it will be created.

    Notes:
        - This function assumes the existence of a Room model with a 'name' field.
        - The `get_or_create` method is used to ensure that duplicate rooms are not created.
    """
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        if room_name:
            room, created = Room.objects.get_or_create(name=room_name)
            if created:
                return Response({'status': 'Room created'})
            else:
                return Response({'status': 'Room already exists'})
            
    return Response({'status': 'Invalid request'})