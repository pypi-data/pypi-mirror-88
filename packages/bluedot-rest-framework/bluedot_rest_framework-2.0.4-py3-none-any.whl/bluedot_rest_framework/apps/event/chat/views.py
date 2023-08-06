
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, user_perform_create, AllView
from .models import EventChat
from .serializers import EventChatSerializer


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
