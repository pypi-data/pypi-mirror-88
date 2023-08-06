import os
from datetime import datetime
from rest_framework.decorators import action
from rest_framework.response import Response
from project.utils.vhall import Vhall
from project.utils.func import md5_str
from .models import EventLivePPT
from .ppt import ppt2images


class LiveView:

    @action(detail=False, methods=['post'], url_path='live-room-create', url_name='live-room-create')
    def live_room_create(self, request, *args, **kwargs):
        _id = request.data.get('event_id', None)
        room_id = Vhall.room_create()
        self.model_class.objects.get(pk=_id).update(
            live__room_id=room_id, live__create_room_time=datetime.now())
        return Response({'room_id': room_id})

    @action(detail=False, methods=['get'], url_path='live-room-token', url_name='live-room-token')
    def live_room_token(self, request, *args, **kwargs):
        _id = request.query_params.get('id', None)
        third_party_user_id = request.query_params.get(
            'third_party_user_id', None)
        queryset = self.model_class.objects.get(pk=_id)
        token = Vhall.get_token(
            room_id=queryset.live['room_id'], third_party_user_id=third_party_user_id)
        queryset.update(live__room_token=token)
        queryset = self.model_class.objects.get(pk=_id)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='live-room-delete', url_name='live-room-delete')
    def room_delete(self, request, *args, **kwargs):
        _id = request.data.get('event_id', None)
        delete_room_id = Vhall.delete_room()
        self.model_class.objects.get(pk=_id).delete(
            live__room_id=delete_room_id)
        return Response({'room_id': delete_room_id})

    @action(detail=False, methods=['post'], url_path='live-room-create-vod', url_name='live-room-create-vod')
    def live_room_create_vod(self, request, *args, **kwargs):
        queryset = self.model_class.objects.get(
            pk=request.data.get('event_id', None))
        print(queryset)
        start_time = str(queryset.live['create_room_time'])[:19]
        end_time = str(datetime.now())[:19]
        vod = Vhall.create_vod(action='SubmitCreateRecordTasks',
                               app_id='b37675d5',
                               stream_id=queryset.live['room_id'],
                               start_time=start_time,
                               end_time=end_time)
        if vod:
            queryset.update(
                live__playback=1, live__vod_id=vod['vod_id'], live__task_id=vod['task_id'])
            return Response({'code': 1})
        return Response({'code': 0})

    @action(detail=False, methods=['get', 'post'], url_path='live-ppt', url_name='live-ppt')
    def live_ppt(self, request, *args, **kwargs):
        if request.method == 'GET':
            event_id = request.query_params.get('event_id')
            queryset = EventLivePPT.objects.filter(event_id=event_id).first()
            if queryset:
                return Response({'image_list': queryset.image_list})
            return Response({'image_list': []})
        elif request.method == 'POST':
            ppt = request.data.get('file')
            event_id = request.data.get('event_id')
            ppt_name = md5_str(
                ppt._name) + '.' + ppt._name.split('.')[-1].strip('"')
            # ppt大小限制20M，部署后nginx也有一个限制
            if ppt and ppt.size > 20480000:
                return Response({'code': 1003, 'msg': 'over size limit'})

            ppt_path = os.getcwd()+'/apps/event/live/tmp_ppt/' + ppt_name
            with open(ppt_path, 'wb') as f:
                data = ppt.read()
                f.write(data)
            print('ppt_path', ppt_path)
            image_list = ppt2images(ppt_path, ppt_name, event_id)
            queryset = EventLivePPT.objects.filter(event_id=event_id).first()
            if queryset:
                queryset.update(image_list=image_list)
            else:
                EventLivePPT.objects.create(
                    event_id=event_id, image_list=image_list)
            return Response({'image_list': image_list})
