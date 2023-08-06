from bluedot_rest_framework.utils.serializers import CustomSerializer
from .models import EventQuestion, EventQuestionUser


class EventQuestionSerializer(CustomSerializer):

    class Meta:
        model = EventQuestion
        fields = '__all__'


class EventQuestionUserSerializer(CustomSerializer):

    class Meta:
        model = EventQuestionUser
        fileds = '__all__'
