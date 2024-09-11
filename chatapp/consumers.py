
from channels.generic.websocket import AsyncWebsocketConsumer

import json
from asgiref.sync import sync_to_async

from django.contrib.auth.models import User
from .models import ChatRoom, ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):

  async def connect(self):
    # to get the room name for url
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.room_group_name = 'chat_%s' % self.room_name

    # code to connect to particular room
    await self.channel_layer.group_add(
      # to add particular room to channel, we need to pass room_group name and channel_name
      self.room_group_name,
      self.channel_name
    )

    await self.accept()
  
  # function to disconnect
  async def disconnect(self, close_code):
    await self.channel_layer.group_discard(
      # remove channel name and group name
      self.channel_name,
      self.room_group_name
    )

  # receives message from websocket
  async def receive(self, text_data):
    data = json.loads(text_data)
    message = data['message']
    username = data['username']
    room = data['room']

    # send this extracted data to channel_layer - group
    await self.channel_layer.group_send(
      # send this message ton particular group so
      self.room_group_name,{
        'type':'chat.message',
        'message':message,
        'username':username,
        'room':room,
      }
    )

    await self.save_message(username, room, message)        # we are calling save message function

  # send message to group
  async def chat_message(self, event):
    message = event['message']
    username = event['username']
    room = event['room']

    # send the above data in json form
    await self.send(text_data = json.dumps({
      'message':message,
      'username':username,
      'room':room,
    }))


  # saving message to database
  @sync_to_async
  def save_message(self, username, room, message):
    user = User.objects.get(username=username)
    room = ChatRoom.objects.get(slug=room)

    ChatMessage.objects.create(user=user, room=room, message_contant=message)


