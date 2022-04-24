"""Collegion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Collegion_Backend import views
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from Collegion import settings
from chat_room.views import get_messages, send_messages


urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    #path('logout/', logout,  name='logout'),
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('chat/', include('Collegion_Backend.urls')),
     # URL form : "/api/messages/1/2"
    path('api/messages/<int:sender>/<int:receiver>/', views.message_list, name='message-detail'),  # For GET request.
    # URL form : "/api/messages/"
    path('api/messages/', views.message_list, name='message-list'),   # For POST
    # URL form "/api/users/1"
    path('api/users/<int:pk>', views.user_list, name='user-detail'),      # GET request for user with id
    path('api/users/', views.user_list, name='user-list'),    # POST for new user and GET for all users list
    path('chat/room/', include('chat_room.urls')),
    path('api/messages/<int:chatroom_id>/', get_messages, name='chat-room-messages'),
    path('api/chat-room/send-messages/', send_messages, name='chat-room-send=messages')
    #path('verification/', include('verify_email.urls')),    #For verifying the emails
]
