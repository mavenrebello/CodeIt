from django.forms import ModelForm

from .models import Question, Answer, Comment

class QuestionForm(ModelForm):
    class Meta:
        model=Question
        exclude=['votes','user']
        #fields='__all__'

class AnswerForm(ModelForm):
    class Meta:
        model=Answer
        exclude=['votes','user', 'question']
        #fields='__all__'