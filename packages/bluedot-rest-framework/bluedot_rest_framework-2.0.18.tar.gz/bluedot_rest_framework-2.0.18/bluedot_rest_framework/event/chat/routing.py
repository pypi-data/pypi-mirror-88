from django.conf.urls import url

from bluedot_rest_framework.settings import api_settings

ChatConsumer = api_settings.EVENT['chat']['consumers']


websocket_urlpatterns = [
    url(r'ws/event/chat/(?P<event_id>\w+)', ChatConsumer),
]
