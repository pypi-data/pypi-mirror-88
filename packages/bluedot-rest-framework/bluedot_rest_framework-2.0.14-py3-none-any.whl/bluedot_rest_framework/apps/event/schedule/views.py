from rest_framework.decorators import action
from rest_framework.response import Response
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet

from .models import EventSchedule
from .serializers import EventScheduleSerializer


class EventScheduleView(CustomModelViewSet):
    model_class = EventSchedule
    serializer_class = EventScheduleSerializer
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
    }

    def create(self, request, *args, **kwargs):
        data = request.data
        ids = list()
        for index, item in enumerate(data['schedule_list']):
            item['sort'] = index
            if 'id' in item:
                ids.append(item['id'])
                self.model_class.objects.get(pk=item['id']).update(
                    project_title=item.get('project_title', None), topic_title=item.get('topic_title', None), speaker_ids=item.get('speaker_ids', None), start_time=item['start_time'], end_time=item['end_time'], sort=item['sort'])
            else:
                queryset = self.model_class.objects.create(
                    project_title=item.get('project_title', None), topic_title=item.get('topic_title', None), speaker_ids=item.get('speaker_ids', None), start_time=item['start_time'], end_time=item['end_time'], sort=item['sort'], event_id=data['event_id'])
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
