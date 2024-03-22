"""
ASGI config for webapps project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapps.settings')

application = get_asgi_application()

import chipcity.routing

application = ProtocolTypeRouter({
    "http": application,
    # urls.py routes for http are added by default
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chipcity.routing.websocket_urlpatterns
        )
    ),
})
