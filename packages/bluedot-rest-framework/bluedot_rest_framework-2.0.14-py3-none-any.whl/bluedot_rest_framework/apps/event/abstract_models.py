from django.db import models


class AbstractEventExtend(models.Model):
    extend_category_id = models.IntegerField()
    extend_video_url = models.TextField(null=True)
    extend_is_banner = models.BooleanField(default=False)
    extend_is_index = models.BooleanField(default=False)

    class Meta:
        abstract = True


class AbstractEventLive(models.Model):
    live_type = models.IntegerField(default=1)
    live_create_room_time = models.DateTimeField(verbose_name='创建房间时间')
    live_room_id = models.CharField(max_length=16, verbose_name='直播房间id')
    live_stream_number = models.CharField(max_length=16, verbose_name='串流码')
    live_push_address = models.CharField(max_length=128, verbose_name='推流地址')
    live_vod_id = models.CharField(max_length=256, verbose_name='回放id')
    live_task_id = models.CharField(max_length=256, verbose_name='任务id')
    live_playback = models.IntegerField(default=0, verbose_name='直播回放')

    class Meta:
        abstract = True


class AbstractEventAddress(models.Model):
    address_country = models.CharField(max_length=32)
    address_province = models.CharField(max_length=32)
    address_city = models.CharField(max_length=32)
    address_info = models.CharField(max_length=255, null=True)
    address_detail_info = models.CharField(max_length=255, null=True)

    class Meta:
        abstract = True
