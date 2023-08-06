from django.db import models


class AbstractEventDataDownload(models.Model):
    event_id = models.IntegerField()

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    data = models.JSONField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class EventDataDownload(AbstractEventDataDownload):

    class Meta:
        db_table = 'event_data_download'
