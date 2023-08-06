from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework.settings import api_settings
from django.utils.module_loading import import_string

EventSpeaker = import_string(api_settings.EVENT['speaker']['models'])


class EventSpeakerSerializer(CustomSerializer):

    class Meta:
        model = EventSpeaker
        fields = '__all__'
