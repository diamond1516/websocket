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


from channels.generic.websocket import AsyncWebsocketConsumer
import json


class OrderStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'order_status_group'
        print(get_channel_layer())
        self.channel_layer = self.channel_layer or get_channel_layer()


        # Groupga qo'shilish
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Groupdan chiqish
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def order_status_changed(self, event):
        # Xabar olish
        message = event['message']

        # Xabar turi, JSON sifatida WebSocket orqali yuboriladi
        await self.send(text_data=json.dumps({
            'type': 'order.status_changed',
            'message': message,
        }))
