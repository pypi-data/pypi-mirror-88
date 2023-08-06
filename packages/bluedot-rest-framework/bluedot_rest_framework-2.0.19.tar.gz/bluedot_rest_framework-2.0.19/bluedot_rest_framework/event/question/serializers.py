from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework.settings import api_settings
from django.utils.module_loading import import_string

EventQuestion = import_string(api_settings.EVENT['question']['models'])
EventQuestionUser = import_string(
    api_settings.EVENT['question']['user_models'])


class EventQuestionSerializer(CustomSerializer):

    class Meta:
        model = EventQuestion
        fields = '__all__'


class EventQuestionUserSerializer(CustomSerializer):

    class Meta:
        model = EventQuestionUser
        fileds = '__all__'
