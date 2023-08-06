from bluedot_rest_framework.utils.serializers import CustomSerializer
from rest_framework.serializers import SerializerMethodField
from .models import EventRegister
from apps.event.models import Event


class EventRegisterSerializer(CustomSerializer):
    event_data = SerializerMethodField()

    class Meta:
        model = EventRegister
        fields = '__all__'

    def get_event_data(self, queryset):

        event_id = queryset.event_id
        event_queryset = Event.objects.filter(pk=event_id).first()
        return {
            "title": event_queryset.title,
            "start_time": event_queryset.start_time,
            "end_time": event_queryset.end_time,
            "banner": event_queryset.banner
        }
