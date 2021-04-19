# import os
#
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# import main.routing
# import django
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TicTacToe.settings')
#
# application = ProtocolTypeRouter({
#   "https": get_asgi_application(),
#   "websocket": AuthMiddlewareStack(
#         URLRouter(
#             main.routing.websocket_urlpatterns
#         )
#     ),
# })

import os
import django
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TicTacToe.settings')
django.setup()
application = get_default_application()