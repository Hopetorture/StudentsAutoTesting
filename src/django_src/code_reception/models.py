import json

from django.contrib.auth.models import User
from django.db import models
from users.models import StudentGroup

from users.models import Profile
from .default_values import CPP_TEMPLATE


# Create your models here.


class Task(models.Model):
    Question_id = models.IntegerField(default=-1)
    title = models.CharField(max_length=100)
    text = models.TextField()
    timeout = models.FloatField(default=3.0)
    user_set = models.ManyToManyField(User)

    def __str__(self):
        return self.title

    def to_question_json(self):
        return {
            "QuestionID": self.Question_id,
            "Title": self.title,
            "Text": self.text,
            "Timeout": self.timeout,
            "testcases": [case.as_dict() for case in self.testcase_set.all()]
        }


class TaskResult(models.Model):
    test = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    solve_status = models.CharField(max_length=20, default='no run')
    status_color = models.CharField(max_length=30, default='red')
    tests_success = models.TextField(max_length=100, default=json.dumps([]))
    submitted_code = models.TextField(max_length=1000, default=CPP_TEMPLATE)


class TestCase(models.Model):
    stdin = models.TextField(default='')
    # filestring input json?
    correct_answer = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"Question title: {self.task.title}, input: {self.stdin}, correct_answer:{self.correct_answer}"

    def as_dict(self):
        return {
            "Test_id": str(self.id),  # do we even need it? mb just dump somewhere later?
            "Stdin_input": str(self.stdin).replace('_', '').split(),
            #"Filestring json": "tbd",
            #"Output_type": "int",
            "Output_value": str(self.correct_answer)
        }


class Course(models.Model):
    tasks_pool = models.ManyToManyField(Task)
    assigned_groups = models.ManyToManyField(StudentGroup)
    users = models.ManyToManyField(User)
    name = models.CharField(max_length=100, default='Новый курс по умолчанию')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_set', null=True)


# class StudentGroup(models.Model):
#     group_name = models.CharField(max_length=30)
    # student = models.ForeignKey(User, on_delete=models.CASCADE)
