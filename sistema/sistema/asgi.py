"""
ASGI config for sistema project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
import sistema.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,                   # Manejo de peticiones HTTP normales
    "websocket": AuthMiddlewareStack(
        URLRouter(
            sistema.routing.websocket_urlpatterns  # Lista de rutas WebSocket
        )
    ),
})
