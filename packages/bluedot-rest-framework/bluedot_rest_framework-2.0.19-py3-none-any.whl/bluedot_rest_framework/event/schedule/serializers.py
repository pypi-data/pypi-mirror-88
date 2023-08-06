from rest_framework.serializers import SerializerMethodField
from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework.settings import api_settings
from django.utils.module_loading import import_string

EventSpeaker = import_string(api_settings.EVENT['speaker']['models'])
EventSpeakerSerializer = import_string(
    api_settings.EVENT['speaker']['serializers'])
EventSchedule = import_string(api_settings.EVENT['schedule']['models'])


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
