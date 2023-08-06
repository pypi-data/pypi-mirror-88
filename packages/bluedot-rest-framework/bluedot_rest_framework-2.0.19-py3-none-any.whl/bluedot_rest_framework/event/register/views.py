from rest_framework.decorators import action
from rest_framework.response import Response

from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, user_perform_create
from bluedot_rest_framework.utils.jwt_token import jwt_get_userid_handler
from bluedot_rest_framework.settings import api_settings
from django.utils.module_loading import import_string

EventRegister = import_string(api_settings.EVENT['register']['models'])
EventRegisterSerializer = import_string(
    api_settings.EVENT['register']['serializers'])


class EventRegisterView(CustomModelViewSet):
    model_class = EventRegister
    serializer_class = EventRegisterSerializer
    filterset_fields = {
        'event_id': {
            'type': 'string',
            'filter': ''
        },
    }

    def perform_create(self, serializer):
        return user_perform_create(self.request.auth, serializer)

    @action(detail=False, methods=['get'], url_path='state', url_name='state')
    def state(self, request, *args, **kwargs):
        event_id = request.query_params.get('event_id', None)
        user_id = jwt_get_userid_handler(self.request.auth)
        queryset = self.model_class.objects.filter(
            user_id=user_id, event_id=event_id).first()
        state = -1
        if queryset:
            state = queryset.state
        return Response({'state': state})
