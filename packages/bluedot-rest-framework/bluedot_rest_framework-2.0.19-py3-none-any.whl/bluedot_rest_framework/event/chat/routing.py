from django.conf.urls import url
from django.utils.module_loading import import_string
from bluedot_rest_framework.settings import api_settings

ChatConsumer = import_string(api_settings.EVENT['chat']['consumers'])


websocket_urlpatterns = [
    url(r'ws/event/chat/(?P<event_id>\w+)', ChatConsumer),
]
