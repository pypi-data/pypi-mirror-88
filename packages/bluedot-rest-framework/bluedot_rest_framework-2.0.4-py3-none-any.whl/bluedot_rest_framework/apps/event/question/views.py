from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, user_perform_create
from rest_framework.response import Response
from apps.event.common.views import CreateUpdateView
from .models import EventQuestionnaire, EventQuestionnaireUser
from .serializers import EventQuestionnaireSerializer, EventQuestionnaireUserSerializer
from bluedot_rest_framework.utils.jwt_token import jwt_get_openid_handler
from rest_framework import status

class EventQuestionnaireView(CustomModelViewSet, CreateUpdateView):
    model_class = EventQuestionnaire
    serializer_class = EventQuestionnaireSerializer
    pagination_class = None

    filterset_fields = {
        '_type': {
            'type': 'int',
            'filter': ''
        },
        'title': {
            'type': 'string',
            'filter': '__contains'
        },
        'event_id': {
            'type': 'string',
            'filter': ''
        },

    }
    def create(self, request, *args, **kwargs):
        event_id=self.request.data.get('event_id', None)
        queryset=self.model_class.objects.filter(event_id=event_id).first()
        if queryset:
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(queryset, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            

    def list(self, request, *args, **kwargs):
        event_id = request.query_params.get('event_id', None)
        queryset = self.model_class.objects.filter(event_id=event_id).first()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class EventQuestionnaireUserView(CustomModelViewSet):
    model_class = EventQuestionnaireUser
    serializer_class = EventQuestionnaireUserSerializer
    filterset_fields = {
        'event_id': {
            'type': 'string',
            'filter': ''
        }

    }

    def list(self, request, *args, **kwargs):
        event_id = request.query_params.get('event_id', None)
        openid = jwt_get_openid_handler(request.auth)
        data = EventQuestionnaireUser.objects.filter(
            event_id=event_id, openid=openid).first()
        if data:
            serializer = self.get_serializer(data)
            return Response({'code': '1', 'data': serializer.data})
        else:
            return Response({'code': '0'})

    def perform_create(self, serializer):
        return user_perform_create(self.request.auth, serializer)
