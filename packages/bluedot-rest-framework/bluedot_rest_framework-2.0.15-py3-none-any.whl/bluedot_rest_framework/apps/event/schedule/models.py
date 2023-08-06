from django.db import models


class AbstractEventSchedule(models.Model):
    event_id = models.IntegerField()

    project_title = models.CharField(max_length=255, verbose_name='项目名称')
    topic_title = models.CharField(max_length=255, verbose_name='互动话题名称')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    sort = models.IntegerField(default=0)

    speaker_ids = models.JSONField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class EventSchedule(AbstractEventSchedule):

    class Meta:
        db_table = 'event_schedule'
