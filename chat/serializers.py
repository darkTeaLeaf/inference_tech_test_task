from django.contrib.auth.models import User
from rest_framework import serializers

from chat.models import Message


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for User model"""
    password = serializers.CharField(write_only=True, help_text='Required. Password must contain at least 8 characters')

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
        write_only_fields = ('password',)
        extra_kwargs = {
            'email': {
                'help_text': 'Email address of a user'
            },
            'first_name': {
                'help_text': 'Name of a user'
            },
            'last_name': {
                'help_text': 'Surname of a user'
            }
        }


class MessageSerializer(serializers.ModelSerializer):
    """ Serializer for Message model"""
    sender = serializers.SlugRelatedField(many=False, slug_field='username', read_only=True)
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'text', 'timestamp']
        read_only_fields = ('sender', 'receiver')
        extra_kwargs = {
            'text': {
                'help_text': 'Message text'
            }
        }
