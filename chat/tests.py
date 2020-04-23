import json

from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from django.test import TestCase
from chat.models import Message
from chat.serializers import MessageSerializer


class MessagesTest(TestCase):
    """ Test module for message API"""

    def setUp(self):
        self.user_1 = User.objects.create(username='arina')
        self.user_1.set_password('admin')
        self.user_1.save()

        self.user_2 = User.objects.create(username='alex')
        self.user_2.set_password('admin')
        self.user_2.save()

        Message.objects.create(
            sender=self.user_1, receiver=self.user_2, text='Hello!')
        Message.objects.create(
            sender=self.user_2, receiver=self.user_1, text='Hi! How are you?')
        Message.objects.create(
            sender=self.user_2, receiver=self.user_2, text='Some important text')

    def test_list_messages(self):
        self.client.login(username=self.user_1.username, password='admin')

        # get API response
        response = self.client.get('/users/' + str(self.user_2.id) + '/messages/')
        # get data from db

        messages = Message.objects.filter((Q(sender=self.user_1) & Q(receiver_id=self.user_2.id))
                                          | (Q(receiver=self.user_1) & Q(sender_id=self.user_2.id)))
        serializer = MessageSerializer(messages, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_message(self):
        self.client.login(username=self.user_1.username, password='admin')
        message_to_display = 1

        response = self.client.get('/users/' + str(self.user_2.id) + '/messages/' + str(message_to_display) + '/')

        message = Message.objects.get(id=message_to_display)
        serializer = MessageSerializer(message)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_message(self):
        self.client.login(username='arina', password='admin')
        message_to_display = 2

        response = self.client.get('/users/' + str(self.user_2.id) + '/messages/' + str(message_to_display) + '/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_message(self):
        self.client.login(username='arina', password='admin')
        data = {'text': 'Great'}

        response = self.client.post('/users/' + str(self.user_2.id) + '/messages/',
                                    data=json.dumps(data),
                                    content_type='application/json')

        self.assertEqual(response.data['sender'], 'arina')
        self.assertEqual(response.data['receiver'], 'alex')
        self.assertEqual(response.data['text'], 'Great')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_valid_update_message(self):
        self.client.login(username='arina', password='admin')
        data = {'text': 'Hello, Alex!'}
        message_to_edit = 1

        response = self.client.patch('/users/' + str(self.user_2.id) + '/messages/' + str(message_to_edit) + '/',
                                     data=json.dumps(data),
                                     content_type='application/json')

        message = Message.objects.get(id=message_to_edit)
        serializer = MessageSerializer(message)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.data['text'], 'Hello, Alex!')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_message(self):
        self.client.login(username='arina', password='admin')
        data = {'text': 'Edit your message'}
        message_to_edit = 2

        response = self.client.patch('/users/' + str(self.user_2.id) + '/messages/' + str(message_to_edit) + '/',
                                     data=json.dumps(data),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_delete_message(self):
        self.client.login(username='arina', password='admin')
        message_to_delete = 1

        response = self.client.delete('/users/' + str(self.user_2.id) + '/messages/' + str(message_to_delete) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_message(self):
        self.client.login(username='arina', password='admin')
        message_to_delete = 2

        response = self.client.delete('/users/' + str(self.user_2.id) + '/messages/' + str(message_to_delete) + '/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
