from django.conf.urls import url

from .consumers import ChatConsumer

websocket_urlpatterns = [
    url(r'ws/event/chat/(?P<event_id>\w+)', ChatConsumer),
]
