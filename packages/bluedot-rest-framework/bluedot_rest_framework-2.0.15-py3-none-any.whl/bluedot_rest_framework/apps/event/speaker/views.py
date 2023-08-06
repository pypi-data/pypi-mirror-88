from rest_framework.decorators import action
from rest_framework.response import Response
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet

from .models import EventSpeaker
from .serializers import EventSpeakerSerializer


class EventSpeakerView(CustomModelViewSet):
    model_class = EventSpeaker
    serializer_class = EventSpeakerSerializer
    pagination_class = None

    filterset_fields = {
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
        data = request.data
        ids = list()
        for index, item in enumerate(data['speaker_list']):
            item['sort'] = index
            if 'id' in item:
                ids.append(item['id'])
                self.model_class.objects.get(pk=item['id']).update(
                    description=item.get('description', ''), img=item.get('img', ''), jobs=item.get('jobs', ''), name=item.get('name', ''), sort=item['sort'], is_sign_page=item.get('is_sign_page', False))
            else:
                queryset = self.model_class.objects.create(
                    description=item.get('description', ''), img=item.get('img', ''), jobs=item.get('jobs', ''), name=item.get('name', ''), sort=item['sort'], is_sign_page=item.get('is_sign_page', False), event_id=data['event_id'])
                ids.append(str(queryset.pk))
        self.model_class.objects.filter(
            id__nin=ids, event_id=data['event_id']).delete()
        queryset = self.model_class.objects.filter(
            event_id=data['event_id']).order_by('sort')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='sort', url_name='sort')
    def sort(self, request, *args, **kwargs):
        before_sort = request.data.get('before_sort')
        before_id = request.data.get('before_id')
        after_sort = request.data.get('after_sort')
        after_id = request.data.get('after_id')
        self.model_class.objects.get(pk=before_id).update(sort=after_sort)
        self.model_class.objects.get(pk=after_id).update(sort=before_sort)
        return Response(status=200)
