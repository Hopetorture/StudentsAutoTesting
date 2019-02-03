import json
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# tasks =[
#     {
#         'Question_id': '42',
#         'Title': 'Sorting',
#         'Text': 'this is a task',
#         'Timeout': '3',
#         'status': 'fail',
#         'status_color': 'red',
#         'test_success': ['True', 'True', 'False']
#     }]

#class TestSuccessField(models.CharField):


class Task(models.Model):
    Question_id = models.IntegerField(default=-1)
    title = models.CharField(max_length=100)
    text = models.TextField()
    timeout = models.FloatField(default=3.0)
    solve_status = models.CharField(max_length=20, default='no run')
    status_color = models.CharField(max_length=30, default='red')
    tests_success = models.TextField(max_length=100, default=json.dumps([]))
    user_set = models.ManyToManyField(User)

    def __str__(self):
        return self.title

# class Student(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     tasks = models.ManyToManyField(Task)
