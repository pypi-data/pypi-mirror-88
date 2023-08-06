from django.db import models


class AbstractUser(models.Model):
    wechat_id = models.IntegerField()
    unionid = models.CharField(max_length=100)
    openid = models.CharField(max_length=100)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    tel = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    job = models.CharField(max_length=100)

    country = models.CharField(max_length=100)
    source_type = models.CharField(max_length=100, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        swappable = 'FORNTEND_USER_MODEL'
        abstract = True


class BaseUser(AbstractUser):

    class Meta(AbstractUser.Meta):
        db_table = 'user'
