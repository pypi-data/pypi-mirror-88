from django.db import models


class WeChatUser(models.Model):
    openid = models.CharField()
    unionid = models.CharField()
    nickname = models.CharField()
    sex = models.IntegerField()
    language = models.CharField()
    city = models.CharField()
    province = models.CharField()
    country = models.CharField()
    headimgurl = models.CharField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wechat_user'
