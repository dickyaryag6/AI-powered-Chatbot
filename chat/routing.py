from django.urls import re_path

from . import consumers

websocket_urlpatterns_web = [
    re_path(r'ws/web/chat/(?P<room_name>\w+)/$', consumers.WebChatConsumer),
]
