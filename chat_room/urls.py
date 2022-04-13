from django.urls import path
from .views import create_chat_room, delete_chat_room, get_all_chat_rooms, invite_to_chat_room, \
    remove_from_chat_room

urlpatterns = [
    path('get-all/<int: user_id>/', get_all_chat_rooms, name='get-all-chatrooms'),
    path('create/', create_chat_room, name='create-chatroom'),
]