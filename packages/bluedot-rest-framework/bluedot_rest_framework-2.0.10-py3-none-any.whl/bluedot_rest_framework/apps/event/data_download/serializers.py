from bluedot_rest_framework.utils.serializers import CustomSerializer
from .models import EventDataDownload


class EventDataDownloadSerializer(CustomSerializer):

    class Meta:
        model = EventDataDownload
        fields = '__all__'
