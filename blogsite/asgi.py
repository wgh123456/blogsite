"""
ASGI config for blogsite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
# add
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogsite.settings')
# ban
# application = get_asgi_application()


application = ProtocolTypeRouter({

    '''
        This root routing configuration specifies that 
        when a connection is made to the Channels development server,
        the ProtocolTypeRouter will first inspect the type of connection. 
        If it is a WebSocket connection (ws:// or wss://), 
        the connection will be given to the AuthMiddlewareStack.
    '''
    
    "http": get_asgi_application(),

    # 在这里指定websocket协议交由特定的路由来处理
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    )
})
