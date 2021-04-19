import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import main.routing
import django
django.setup()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TicTacToe.settings')

application = ProtocolTypeRouter({
  "https": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            main.routing.websocket_urlpatterns
        )
    ),
})

