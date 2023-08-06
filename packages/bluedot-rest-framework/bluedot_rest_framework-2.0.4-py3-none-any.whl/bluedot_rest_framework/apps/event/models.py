from django.db import models
from .abstract_models import AbstractEventExtend, AbstractEventLive, AbstractEventAddress


class AbstractEvent(AbstractEventExtend, AbstractEventLive, AbstractEventAddress):
    event_type = models.IntegerField(default=1)
    is_show = models.IntegerField(default=0)

    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255, null=True)
    description = models.CharField(verbose_name='介绍')

    banner = models.CharField(max_length=255, verbose_name='封面图片')
    qr_code = models.CharField(max_length=255, verbose_name='二维码')

    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')

    module_list = models.JSONField(verbose_name='模块列表')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Event(AbstractEvent):
    class Meta:
        db_table = 'event'
