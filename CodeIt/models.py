from django.db import models
from django.contrib.auth.models import User

# Create your models here.
  

class Question(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic=models.CharField(max_length=300, null=True)
    header=models.CharField(max_length=300)
    body=models.TextField(null=True, blank=True)
    code=models.TextField(null=True, blank=True)
    votes=models.IntegerField(default=0)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return self.header

class Answer(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    body=models.TextField()
    code=models.TextField(null=True, blank=True)
    votes=models.IntegerField(default=0)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]
    
class Comment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    answer=models.ForeignKey(Answer, on_delete=models.CASCADE)
    body=models.TextField()
    votes=models.IntegerField(default=0)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
