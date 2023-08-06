
from datetime import datetime
from rest_framework.decorators import action
from rest_framework.response import Response
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, AllView
from bluedot_rest_framework.utils.jwt_token import jwt_get_userid_handler
from bluedot_rest_framework.utils.func import get_tree
from bluedot_rest_framework.utils.area import area
from bluedot_rest_framework.settings import api_settings
from .live.views import LiveView
from .frontend_views import FrontendView
from django.utils.module_loading import import_string

EventRegister = import_string(api_settings.EVENT['register']['models'])
Event = import_string(api_settings.EVENT['models'])
EventSerializer = import_string(api_settings.EVENT['serializers'])


class EventView(CustomModelViewSet, FrontendView, LiveView, AllView):
    model_class = Event
    serializer_class = EventSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        date_now = datetime.now()
        if instance.start_time > date_now:
            instance.update(state=1)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        elif instance.start_time < date_now and instance.end_time > date_now:
            instance.update(state=2)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        elif instance.end_time < date_now:
            instance.update(state=3)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='area', url_name='area')
    def area(self, request, *args, **kwargs):
        return Response(area)
