from django.urls import path
import Collegion_Backend.views as views

app_name = 'Collegion_Backend'


urlpatterns = [
    path('', views.chat_view, name='chats'),
    path('<int:sender>/<int:receiver>/', views.message_view, name='message_view'),
]