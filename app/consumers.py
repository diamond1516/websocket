# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.consumer import SyncConsumer
from channels.layers import get_channel_layer


class SomeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'salom'
        self.channel_layer = self.channel_layer or get_channel_layer()

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

        # channel_layer obyektini saqlang
        self.scope['channel_layer'] = self.channel_layer

        await self.send(text_data=json.dumps({'msg': 'salom'}))
        print(self.scope.get('user'))

    async def disconnect(self, close_code):
        await self.send(text_data=json.dumps({
            'msg': 'disconnect'
        }))
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['msg']

        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def notification_send(self, event):
        await self.send(
            {"action": "new_notification", "data": event["data"]}
        )


