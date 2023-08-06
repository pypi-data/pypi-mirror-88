from django.db import models
from .abstract_models import AbstractQuestion, AbstractQuestionUser


class Question(AbstractQuestion):

    title = models.CharField(max_length=100)
    integral = models.IntegerField(default=0, max_length=100)
    qa = models.JSONField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'question'


class QuestionUser(AbstractQuestionUser):
    qa_id = models.IntegerField(max_length=100)
    user_id = models.IntegerField(max_length=11)
    openid = models.CharField(max_length=100)
    unionid = models.CharField(max_length=100)

    title = models.CharField(max_length=100)
    integral = models.IntegerField(default=0, max_length=100)

    qa = models.JSONField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'question_user'
