from django.urls import path
from chipcity import consumers
app_name = "ChipCity"


websocket_urlpatterns = [
    path('table/data', consumers.MyConsumer.as_asgi()),
]