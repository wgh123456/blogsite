from django.urls import re_path

from. import consumers

websocket_urlpatterns = [
    # 使用consumers.ChatConsumer.as_asgi()为每个链接建立一个consumer实例
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi())
]