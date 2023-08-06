from bluedot_rest_framework.utils.serializers import CustomSerializer
from .models import EventChat


class EventChatSerializer(CustomSerializer):

    class Meta:
        model = EventChat
        fields = '__all__'
