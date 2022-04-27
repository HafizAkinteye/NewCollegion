from django.shortcuts import render, get_object_or_404
from tkinter.tix import Form
import email
from django.shortcuts import render, redirect
from django.contrib.auth.models import User                                # Django Build in User Model
from django.contrib.auth import authenticate, login #Django's inbuilt authentication methods
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from Collegion_Backend.models import DMMessage                                               # Our Message model
from Collegion_Backend.serializers import MessageSerializer, UserSerializer # Our Serializer Classes
from django.http import HttpResponse
from django.core.mail import EmailMessage
from chat_room.models import ChatRoom
from random import randint
from django.core.mail import send_mail
from django.conf import settings
from verify_email.email_handler import send_verification_email
import re


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
        #try:
        user = User.objects.create_user(username=data['username'], email = data['email'], password=data['password'])
        random_int = randint(100, 999)
        user.profile.anonymous_name = "Anonymous"+str(random_int)+str(user.id)
        user.save()

        user.is_active = False
        print("user email")
        print(user.email)

        match = re.match('^[a-zA-Z0-9.!#$%&\'*+=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[e][d][u](?:[e][d][u]{0,61}[a-zA-Z0-9])?)*$', user.email)
        print(match)
        if match == None:
            print('Email is not edu email') #change to show up on register.html and prevent the user to being created
        else:
            print('Email is an edu email')
            print(user.email)
            email_subject = 'Account verification needed'
            email_body = 'Test body'
            print("we made it to x")
            #if user.is_active():
            #   inactive_user = send_verification_email(request, user)
            print("we made it to y")
            send_mail(
            email_subject,
            email_body,
            'collegionapp@gmail.com',
            [user.email],
            fail_silently=False,
            )

        return JsonResponse(data, status=201)
        #except Exception as e:
            #return JsonResponse({'error': "Something went wrong: {e}"}, status=400)


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
        regex = '@((\w+)[.]?)+'
        user_domain = re.search(regex, request.user.email)
        if user_domain.group() == re.search(regex, other_user.email).group() and not other_user == user:
            if other_user not in user.profile.dm_users.all():
                user.profile.dm_users.add(other_user)
                user.save()
            if user not in other_user.profile.dm_users.all():
                other_user.profile.dm_users.add(user)
                other_user.save()
        messages = DMMessage.objects.filter(sender_id=sender, receiver_id=receiver) | \
                                   DMMessage.objects.filter(sender_id=receiver, receiver_id=sender)
        for msg in messages:
            if not msg.is_read:
                msg.is_read = True
                msg.save()
        return render(request, "chat/messages.html",
                      {'users': User.objects.exclude(username=request.user.username), #List of users
                       'sender': other_user,
                       'receiver': User.objects.get(id=receiver),
                       'chatroom': ChatRoom.objects.all().filter(member=request.user.id),
                       'messages': messages,
                       'is_message': True,
                       'direct_messages': request.user.profile.dm_users.all()}) # Return context with message objects where users are either sender or receiver.

@csrf_exempt
def add_dm_user_form(request):
    if not request.user.is_authenticated:
        return redirect('index')
    regex = '@((\w+)[.]?)+'
    user_domain = re.search(regex, request.user.email)
    dm_users = request.user.profile.dm_users.all()
    if request.method == "POST":
        user_ls = []
        users = list(User.objects.all())
        query = request.POST.get("search")
        for user in users:
            if query in user.username and user not in dm_users \
                    and user_domain.group() == re.search(regex, user.email).group():
                user_ls.append(user)
    else:
        user_ls = []
        for user in list(request.user.profile.dm_users.all()):
            if not user in dm_users and user_domain.group() == re.search(regex, user.email).group():
                user_ls.append(user)

    return render(request, "chat/add-dm.html",
                  {
                      'search_users': user_ls,
                      'chatroom': ChatRoom.objects.all().filter(member=request.user.id),
                      'direct_messages': request.user.profile.dm_users.all()})

def dm_add(request, user_id):
    userToAdd = User.objects.get(id=user_id)
    user = request.user
    user.profile.dm_users.add(userToAdd)

    return redirect("/chat/add-dm-form/")