from django.contrib.auth.models import User
from django.db import models
from chat_room import ChatRoom


class Message(models.Model):
     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', null=True)
     chat_room = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL, related_name='chat_room', null=True)
     message = models.CharField(max_length=1200)
     timestamp = models.DateTimeField(auto_now_add=True)
     is_read = models.BooleanField(default=False)
     def __str__(self):
           return self.message
     class Meta:
           ordering = ('timestamp',)


