import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import requests


def call_chatbot_api(message):
    # call chatbot api
    host = "localhost"
    port = "8000"
    url = "http://" + host + ":" + port + "/api/chatterbot/"

    body = {"text": message}

    response = requests.post(url, json=body)
    answer = response.json()['response']
    return answer


class WebChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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

    # fungsi receive dipanggil ketika ada pesan masuk
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        # time

        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({'message': message}))

        answer = call_chatbot_api(message)

        self.send(text_data=json.dumps({'message': answer}))



