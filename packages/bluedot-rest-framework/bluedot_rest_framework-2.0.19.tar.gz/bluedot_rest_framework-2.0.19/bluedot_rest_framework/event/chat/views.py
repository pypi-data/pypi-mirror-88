
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, user_perform_create, AllView
from bluedot_rest_framework.settings import api_settings
from django.utils.module_loading import import_string
EventChat = import_string(api_settings.EVENT['chat']['models'])
EventChatSerializer = import_string(api_settings.EVENT['chat']['serializers'])


class EventChatView(CustomModelViewSet, AllView):
    model_class = EventChat
    serializer_class = EventChatSerializer
    filterset_fields = {
        'state': {
            'type': 'int',
            'filter': ''
        },
        'event_id': {
            'type': 'string',
            'filter': ''
        }

    }

    def perform_create(self, serializer):
        return user_perform_create(self.request.auth, serializer)
