from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from Collegion_Backend.models import GroupMessage
from chat_room.models import ChatRoom
from chat_room.serializers import ChatRoomMessageSerializer, GetChatRoomMessageSerializer
import re



# Create your views here.
def add_user(request, group_id, user_to_add_id):
    username = request.user.username
    userToAdd = User.objects.get(id=user_to_add_id)
    chatRoom = ChatRoom.objects.get(id=group_id)
    chatRoom.member.add(userToAdd)

    return redirect("/chat/room/addUserForm/"+str(group_id))

@csrf_exempt
def add_user_form(request, group_id):
    if not request.user.is_authenticated:
        return redirect('index')
    regex = '@((\w+)[.]?)+'
    user_domain = re.search(regex, request.user.email)
    group_chat = ChatRoom.objects.get(id=group_id)
    if request.method == "POST":
        user_ls = []
        users = list(User.objects.all())
        query = request.POST.get("search")
        for user in users:
            if query in user.username and user not in group_chat.member.all() \
                    and re.search(regex, user.email) is not None \
                    and user_domain.group() == re.search(regex, user.email).group():
                user_ls.append(user)
    else:
        user_ls = []
        for user in list(request.user.profile.dm_users.all()):
            if not user in group_chat.member.all() \
                and re.search(regex, user.email) is not None \
                and user_domain.group() == re.search(regex, user.email).group():
                user_ls.append(user)

    return render(request, "chat/add-to-group.html",
                  {
                   'search_users': user_ls,
                   'chatroom': ChatRoom.objects.all().filter(member=request.user.id),
                   'direct_messages': request.user.profile.dm_users.all(),
                   'group': group_id})

def create_chat_room(request):
    if not request.user.is_authenticated:
        return redirect('index')
    dm_users = request.user.profile.dm_users.all()
    user_ls = dm_users
    err_msg = ""
    if request.method == "POST":
        print(request.POST)
        group_name = request.POST.get("name")
        if group_name == "":
            err_msg = "Please insert a name for your Group Chat."
        else:
            group_chat = ChatRoom.objects.create(name=group_name, creator=request.user)
            group_chat.member.add(request.user)
            group_chat.save()



    return render(request, "chat/create-chatroom.html",
                  {'is_createChatroom': True,
                   'search_users': user_ls,
                   'chatroom': ChatRoom.objects.all().filter(member=request.user.id),
                   'direct_messages': dm_users,
                   'error': err_msg})

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
        serializer = GetChatRoomMessageSerializer(messages, many=True, context={'request': request})
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
        chat_room = ChatRoom.objects.get(id=chatroom_id)
        if request.user.profile.is_anonymous:
            anonymous = "true"
        else:
            anonymous = "false"
        group_messages = GroupMessage.objects.all().filter(chat_room=chatroom_id)
        for msg in group_messages:
            if request.user not in msg.is_read.all():
                msg.is_read.add(request.user)
                msg.save()

        return render(request, "chat/messages.html",
                      {'chatroom_id': chatroom_id,
                       'anonymous_str': anonymous,
                       'is_anonymous': request.user.profile.is_anonymous,
                       'group_name': chat_room.name,
                       'is_chatroom': True,
                       'chatroom': ChatRoom.objects.all().filter(member=request.user.id),
                       'messages': GroupMessage.objects.all().filter(chat_room=chatroom_id, is_read=request.user.id),
                       'direct_messages': request.user.profile.dm_users.all()})

@csrf_exempt
def anonymous_handle(request):
    request.user.profile.is_anonymous = not request.user.profile.is_anonymous
    request.user.save()
    return redirect(request.POST.get("next"))

def remove_from_chat_room(request, room_id):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        chat_room = ChatRoom.objects.get(id=room_id)
        chat_room.member.remove(request.user)
        return redirect('index')

