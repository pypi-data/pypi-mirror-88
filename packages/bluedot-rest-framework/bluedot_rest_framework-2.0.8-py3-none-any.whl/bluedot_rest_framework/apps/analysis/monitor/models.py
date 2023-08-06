from django.db import models


class AnalysisMonitor(models.Model):
    _type = models.CharField(max_length=255)

    user_unionid = models.CharField(max_length=100)
    user_openid = models.CharField(max_length=100)
    user_ip = models.CharField(max_length=100)
    user_network = models.CharField(max_length=100)
    user_agent = models.JSONField()

    page_title = models.CharField(null=True)
    page_keywords = models.JSONField()
    page_description = models.CharField(null=True)

    page_url = models.CharField(null=True)
    page_base_url = models.CharField(null=True)
    page_param = models.JSONField(null=True)

    page_event_key = models.CharField(max_length=255)
    page_event_type = models.CharField(max_length=100)

    wechat_user_name = models.CharField(null=True)
    wechat_appid = models.CharField(null=True)
    wechat_name = models.CharField(null=True)
    wechat_event_key = models.CharField(null=True)
    wechat_event_msg = models.CharField(null=True)
    wechat_event_type = models.CharField(null=True)
    wechat_label = models.CharField(null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'analysis_monitor'
