from django.urls import path
from poker import consumers

websocket_urlpatterns = [
    path('poker/data', consumers.MyConsumer.as_asgi()),
]