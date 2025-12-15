# from django.urls import re_path
# from . import consumers

# websocket_urlpatterns = [
#     # Match room_id (can be numeric or alphanumeric) with optional trailing slash
#   re_path(
#     r'^websocket/chat/(?P<room_id>[^/]+)/?$',
#     consumers.ChatConsumer.as_asgi()
# )

# ]



from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(
        r'^websocket/chat/(?P<room_id>[^/]+)/?$',
        ChatConsumer.as_asgi()
    ),
]
