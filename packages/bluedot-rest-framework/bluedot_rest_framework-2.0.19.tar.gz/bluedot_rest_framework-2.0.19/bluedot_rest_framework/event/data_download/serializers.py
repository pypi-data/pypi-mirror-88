from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework.settings import api_settings
from django.utils.module_loading import import_string

EventDataDownload = import_string(
    api_settings.EVENT['data_download']['models'])


class EventDataDownloadSerializer(CustomSerializer):

    class Meta:
        model = EventDataDownload
        fields = '__all__'
