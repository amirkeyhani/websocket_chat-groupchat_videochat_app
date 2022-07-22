from django.urls import path

from .consumers import ChatConsumer
from .custom_consumer import CustomChatConsumer, EchoConsumer

websocket_urlpatterns = [
    path('ws/', EchoConsumer.as_asgi()), 
    path('ws/echo/chat/<str:username>/', ChatConsumer.as_asgi()),
    path('ws/echo/chat2/<str:username>/', CustomChatConsumer.as_asgi()),
]