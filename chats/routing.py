from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]

ASGI_APPLICATION = "Channels_test_project.routing.application"