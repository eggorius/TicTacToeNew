import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *


class GameConsumer(WebsocketConsumer):

    http_user = True

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['game_name']
        self.room_group_name = 'game_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        cell = text_data_json['cell']
        turn = text_data_json['turn']
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'game_message',
                'message': message,
                'cell': cell,
                'turn': turn,
            }
        )

    # Receive message from room group
    def game_message(self, event):
        message = event['message']
        cell = event['cell']
        turn = event['turn']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'cell': cell,
            'turn': turn,
        }))
