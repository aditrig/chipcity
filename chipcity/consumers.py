from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class MyConsumer(WebsocketConsumer):
    group_name = 'todolist_group'
    channel_name = 'todolist_channel'

    user = None

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )

        self.accept()

        if not self.scope["user"].is_authenticated:
            self.send_error(f'You must be logged in')
            self.close()
            return      

        self.user = self.scope["user"]

        self.broadcast_list()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )

    # def receive(self, **kwargs):
    #     if 'text_data' not in kwargs:
    #         self.send_error('you must send text_data')
    #         return

    #     try:
    #         data = json.loads(kwargs['text_data'])
    #     except json.JSONDecoder:
    #         self.send_error('invalid JSON sent to server')
    #         return

    #     if 'action' not in data:
    #         self.send_error('action property not sent in JSON')
    #         return

    #     action = data['action']

    #     if action == 'add':
    #         self.received_add(data)
    #         return

    #     if action == 'delete':
    #         self.received_delete(data)
    #         return

    #     self.send_error(f'Invalid action property: "{action}"')
