from bluedot_rest_framework.utils.serializers import CustomSerializer
from .models import Event


class EventSerializer(CustomSerializer):

    class Meta:
        model = Event
        fields = '__all__'
