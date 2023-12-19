# routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from app import consumers

websocket_urlpatterns = [
    # Misol uchun:
    path("ws/some_path/", consumers.SomeConsumer.as_asgi()),
]
