from django.contrib.auth.models import User
from rest_framework import serializers
from Collegion_Backend.models import GroupMessage


class ChatRoomMessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())

    class Meta:
        model = GroupMessage
        fields = ['sender', 'chat_room', 'message', 'timestamp', 'anonymous', 'display_name']


class GetChatRoomMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupMessage
        fields = ['display_name', 'chat_room', 'message', 'timestamp', 'anonymous']