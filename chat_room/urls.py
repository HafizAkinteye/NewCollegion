from django.urls import path
from .views import create_chat_room, delete_chat_room, message_chat_view, invite_to_chat_room, \
    remove_from_chat_room, add_user_form, add_user

app_name = 'chat_room'

urlpatterns = [
    path('<int:chatroom_id>/', message_chat_view, name='message-chatrooms'),
    path('create/', create_chat_room, name='create-chatroom'),
    path('addUserForm/<int:group_id>/', add_user_form, name = 'add-to-group' ),
    path('addUser/<int:group_id>/<int:user_id>/', add_user, name = 'add-user' )
]
