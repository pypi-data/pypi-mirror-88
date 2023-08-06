from rest_framework.serializers import SerializerMethodField

from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework.apps.event.speaker.models import EventSpeaker
from bluedot_rest_framework.apps.event.speaker.serializers import EventSpeakerSerializer
from .models import EventSchedule


class EventScheduleSerializer(CustomSerializer):

    speaker_user = SerializerMethodField()

    class Meta:
        model = EventSchedule
        fields = '__all__'

    def get_speaker_user(self, queryset):
        if queryset.speaker_ids:
            speaker_user_queryset = EventSpeaker.objects.filter(
                pk__in=queryset.speaker_ids)
            return EventSpeakerSerializer(speaker_user_queryset, many=True).data
        return []
