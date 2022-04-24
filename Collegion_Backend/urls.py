from django.urls import path
import Collegion_Backend.views as views

app_name = 'Collegion_Backend'


urlpatterns = [
    path('', views.chat_view, name='chats'),
    path('<int:sender>/<int:receiver>/', views.message_view, name='message_view'),
    path('add-dm-form/', views.add_dm_user_form, name="add-dm-user-form"),
    path('dm-add/<int:user_id>/', views.dm_add, name="dm_add"),
]