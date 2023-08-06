import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import EventChat


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.event_id = self.scope['url_route']['kwargs']['event_id']
        print(self.event_id)
        self.room_group_name = 'chat_%s' % self.event_id

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
        print('text_data_json', text_data_json)

        data = {
            'user_id': text_data_json.get('user_id', None),
            'unionid': text_data_json.get('unionid', None),
            'openid': text_data_json.get('openid', None),
            'nick_name': text_data_json.get('nick_name', None),
            'avatar_url': text_data_json.get('avatar_url', None),
            'event_id': self.event_id,
            'state': text_data_json.get('state', None),

            'data': text_data_json.get('data', None),
        }
        if data["state"] == 0:
            EventChat.objects.create(**data)
        elif data["state"] == 1:
            _id = text_data_json.get('id', None)
            EventChat.objects.get(pk=_id).update(state=1)

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'event_chat_message',
                    **data
                }
            )
        elif data['state'] == 2:
            _id = text_data_json.get('id', None)
            EventChat.objects.get(pk=_id).update(state=2)

    # Receive message from room group

    def event_chat_message(self, event):
        self.send(text_data=json.dumps({
            **event
        }))
