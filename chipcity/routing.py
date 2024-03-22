from django.urls import path
from chipcity import consumers

websocket_urlpatterns = [
    path('poker/data', consumers.MyConsumer.as_asgi()),
]