from django.contrib.auth.models import User
from rest_framework import serializers
from Collegion_Backend.models import Message


class ChatRoomMessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'chat_room', 'message', 'timestamp']