from bluedot_rest_framework.utils.serializers import CustomSerializer
from .models import EventSpeaker


class EventSpeakerSerializer(CustomSerializer):

    class Meta:
        model = EventSpeaker
        fields = '__all__'
