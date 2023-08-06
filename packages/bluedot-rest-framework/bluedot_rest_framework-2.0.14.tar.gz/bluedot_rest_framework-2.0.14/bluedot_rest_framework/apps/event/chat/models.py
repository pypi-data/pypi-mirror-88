from django.db import models


class AbstractEventChat(models.Model):
    event_id = models.IntegerField()

    user_id = models.IntegerField()
    unionid = models.CharField(max_length=32)
    openid = models.CharField(max_length=32)

    nick_name = models.CharField(max_length=100)
    avatar_url = models.CharField(max_length=255)

    state = models.IntegerField(default=0)
    data = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class EventChat(AbstractEventChat):
    class Meta:
        db_table = 'event_chat'
