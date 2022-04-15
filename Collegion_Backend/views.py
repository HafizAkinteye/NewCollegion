from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login #Django's inbuilt authentication methods
from django.shortcuts import render, redirect
from django.contrib.auth.models import User                                # Django Build in User Model
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from Collegion_Backend.models import DMMessage                                               # Our Message model
from Collegion_Backend.serializers import MessageSerializer, UserSerializer # Our Serializer Classes
from django.http import HttpResponse
from django.core.mail import EmailMessage
from chat_room.models import ChatRoom

def index(request):
    if request.user.is_authenticated:
        return redirect('chat/')
    if request.method == 'GET':
        return render(request, 'chat/index.html', {})
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return HttpResponse(render(request, 'chat/index.html', {"error": "Password or Username was incorrect"}))
        return redirect('chat/')


@csrf_exempt
def user_list(request, pk=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        if pk:
            users = User.objects.filter(id=pk)
        else:
            users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            user = User.objects.create_user(username=data['username'], password=data['password'])
            user.save()
            user.is_active = False
            
            email_subject = 'Account verification needed'
            email_body = 'Test body'
            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@collegion.com'
                'saifrock619@gmail.com'
            )
            email.send(fail_silently= False)

            return JsonResponse(data, status=201)
        except Exception:
            return JsonResponse({'error': "Something went wrong"}, status=400)


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = DMMessage.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False).exclude(sender=receiver)

        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def register_view(request):
    """
    Render registration template
    """
    if request.user.is_authenticated:
        return redirect('chats')
    return render(request, 'chat/register.html', {})


def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        active_chatrooms = ChatRoom.objects.all().filter(member=request.user.id)
        for chat in active_chatrooms:
            print(chat.name)
        return render(request, 'chat/chat.html',
                      {'users': User.objects.exclude(username=request.user.username),
                       'chatroom': active_chatrooms,
                       'direct_messages': request.user.profile.dm_users.all()})


#Takes arguments 'sender' and 'receiver' to identify the message list to return
def message_view(request, sender, receiver):
    """Render the template with required context variables"""
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        if request.user.id == sender:
            other_user = get_object_or_404(User, pk=receiver)
        else:
            other_user = get_object_or_404(User, pk=sender)
        user = request.user
        if other_user not in user.profile.dm_users.all():
            user.profile.dm_users.add(other_user)
            user.save()
        if user not in other_user.profile.dm_users.all():
            other_user.profile.dm_users.add(user)
            other_user.save()
        return render(request, "chat/messages.html",
                      {'users': User.objects.exclude(username=request.user.username), #List of users
                       'receiver': User.objects.get(id=receiver),
                       'chatroom': ChatRoom.objects.all().filter(member=request.user.id),
                       'messages': DMMessage.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   DMMessage.objects.filter(sender_id=receiver, receiver_id=sender),
                       'is_message': True,
                       'direct_messages': request.user.profile.dm_users.all()}) # Return context with message objects where users are either sender or receiver.
