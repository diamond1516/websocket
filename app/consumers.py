# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.consumer import SyncConsumer
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer


class SomeConsumer(AsyncWebsocketConsumer):
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

    async def notification_send(self, event):
        data = {"action": "new_notification", "data": event["message"]}
        await self.send(json.dumps(
            {"action": "new_notification", "data": event["message"]})
        )


class OrderStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'order_status_group'
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

    async def salom(self, event):
        # Xabar olish
        message = event['message']

        # Xabar turi, JSON sifatida WebSocket orqali yuboriladi
        await self.send(text_data=json.dumps({
            'type': 'order.status_changed',
            'message': message,
        }))
