from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from chat.models import Message
from chat.permissions import IsOwnerOrReadOnly, IsOwner
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
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        return self.user_serializer


class MessageViewSet(viewsets.ModelViewSet):
    """
        retrieve:
        Return the particular message specified by **id** and belonging to user with id equals to **user_id**.

        list:
        Return a list of messages belonging to user with id equals to **user_id** and somehow related to user which
        credentials are provided with the request (authenticated user is sender or receiver for the messages).

        create:
        Create a new message for user with id equals to **user_id** from  user which credentials are provided
        with the request.

        update:
        Update the message specified by **id** where user with id equals to **user_id** is receiver and user which
        credentials are provided with the request is sender. Request should contain all message parameters.

        partial_update:
        Update some of message fields which specified by **id** where user with id equals to **user_id** is receiver
        and user which credentials are provided with the request is sender. There is no requirement to contain
        all the parameters.

        delete:
        Delete the message specified by **id** where user with id equals to **user_id** is receiver and user which
        credentials are provided with the request is sender.
    """
    message_serializer = MessageSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Get messages of specified user, but related to requesting one
        messages = Message.objects.filter((Q(sender=self.request.user) & Q(receiver_id=self.kwargs['user_id']))
                                          | (Q(receiver=self.request.user) & Q(sender_id=self.kwargs['user_id'])))
        return messages

    def get_serializer_class(self):
        return self.message_serializer

    def perform_create(self, serializer):
        # Specify the sender and receiver automatically according to path parameters and authentication
        return serializer.save(sender=self.request.user, receiver=User.objects.get(id=self.kwargs['user_id']))
