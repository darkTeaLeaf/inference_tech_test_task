from django.contrib.auth.models import User
from rest_framework import serializers

from chat.models import Message


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
        write_only_fields = ('password',)


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username', read_only=True)
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'text', 'timestamp']
        read_only_fields = ('sender', 'receiver')
