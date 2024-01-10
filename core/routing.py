# routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, re_path

from app import consumers
from app.consumers import OrderStatusConsumer

websocket_urlpatterns = [
    # Misol uchun:
    path("ws/some_path/", consumers.SomeConsumer.as_asgi()),
    re_path(r'ws/order_status/$', OrderStatusConsumer.as_asgi()),
]
