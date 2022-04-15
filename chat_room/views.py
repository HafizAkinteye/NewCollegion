from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from Collegion_Backend.models import GroupMessage
from chat_room.models import ChatRoom
from chat_room.serializers import ChatRoomMessageSerializer

# Create your views here.

def create_chat_room(request):
    return render(request, "chat/create-chatroom.html",
                  {'is_createChatroom': True,
                   'chatroom': ChatRoom.objects.all().filter(member=request.user.id),
                   'direct_messages': request.user.profile.dm_users.all()})

def delete_chat_room(request):
    pass

def get_messages(request, chatroom_id):
    """
        List all required messages, or create a new message.
        """
    if request.method == 'GET':
        messages = GroupMessage.objects.filter(chat_room=chatroom_id).exclude(sender=request.user.id) \
        .exclude(is_read=request.user.id)

        for m in messages:
            m.is_read.add(request.user)
            m.save()
        serializer = ChatRoomMessageSerializer(messages, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def send_messages(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ChatRoomMessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def message_chat_view(request, chatroom_id):
    """Render the template with required context variables"""
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, "chat/messages.html",
                      {'chatroom_id': chatroom_id,
                       'is_chatroom': True,
                       'chatroom': ChatRoom.objects.all().filter(member=request.user.id),
                       'messages': GroupMessage.objects.all().filter(chat_room=chatroom_id),
                       'direct_messages': request.user.profile.dm_users.all()})

def invite_to_chat_room(request):
    pass

def remove_from_chat_room(request):
    pass