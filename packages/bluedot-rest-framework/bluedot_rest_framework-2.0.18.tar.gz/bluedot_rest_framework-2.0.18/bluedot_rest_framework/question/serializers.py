from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Question, QuestionUser


class QuestionSerializer(DocumentSerializer):

    class Meta:
        model = Question
        fields = '__all__'


class QuestionUserSerializer(DocumentSerializer):

    class Meta:
        model = QuestionUser
        fields = '__all__'
