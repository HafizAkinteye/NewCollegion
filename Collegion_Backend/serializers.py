from django.contrib.auth.models import User
from rest_framework import serializers
from Collegion_Backend.models import DMMessage
#
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    """For Serializing User"""
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'id', 'first_name', 'last_name']
#
# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    """For Serializing Message"""
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    class Meta:
        model = DMMessage
        fields = ['sender', 'receiver', 'message', 'timestamp']

