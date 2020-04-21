from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets

from chat.models import Message
from chat.serializers import MessageSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
        retrieve:
        Return the user specified by id.

        list:
        Return a list of all the existing users.

        create:
        Create a new user.

        update:
        Update of all user fields. Request should contain all user parameters.

        partial_update:
        Update of all or some of user fields. There is no requirement to contain all the parameters.

        delete:
        Delete the user specified by id.

    """
    queryset = User.objects.all()
    user_serializer = UserSerializer

    def get_serializer_class(self):
        return self.user_serializer


class MessageViewSet(viewsets.ModelViewSet):
    """
        retrieve:
        Return the particular user's message specified by id.

        list:
        Return a list of all the existing messages for or from particular user.

        create:
        Create a new message from particular user.

        update:
        Update of all message fields which send by particular user. Request should contain all message parameters.

        partial_update:
        Update of all or some of message fields which send by particular user. There is no requirement to contain
        all the parameters.

        delete:
        Delete the particular user's message specified by id.

    """
    message_serializer = MessageSerializer

    def get_queryset(self):
        messages = Message.objects.filter(Q(sender_id=self.kwargs['user_id']) | Q(receiver_id=self.kwargs['user_id']))
        return messages

    def get_serializer_class(self):
        return self.message_serializer
