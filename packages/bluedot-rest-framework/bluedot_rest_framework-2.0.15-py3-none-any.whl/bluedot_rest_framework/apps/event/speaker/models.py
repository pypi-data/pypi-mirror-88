from django.db import models


class AbstractEventSpeaker(models.Model):
    event_id = models.IntegerField()
    name = models.CharField(max_length=255)
    jobs = models.CharField(max_length=255)
    description = models.TextField()
    img = models.CharField(max_length=255)
    is_sign_page = models.BooleanField(default=False)
    sort = models.IntegerField(default=1)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class EventSpeaker(AbstractEventSpeaker):

    class Meta:
        db_table = 'event_speaker'
