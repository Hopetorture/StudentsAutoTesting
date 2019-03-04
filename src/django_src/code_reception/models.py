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

#TODO !!!
# Отделить entity task от entity Result, так как Task - один на всех, а result у каждого разный

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

    def to_question_json(self):
        return {
            "QuestionID": self.Question_id,
            "Title": self.title,
            "Text": self.text,
            "Timeout": self.timeout,
            "testcases": [case.as_dict() for case in self.testcase_set.all()]
        }
    # question_json = {
    #     "QuestionID": task.Question_id,
    #     "Title": task.title,  # possible to cut it?
    #     "Text": task.text,
    #     "Timeout": task.timeout,
    #     "testcases":
    #         [{
    #             "Test_id": "1",
    #             "Stdin_input": ["3", "3"],
    #             "Filestring json": "formatted string with test data input",
    #             "Output_type": "string",
    #             "Output_value": "Hello world"
    #         },
    #             {
    #                 "Test_id": "2",
    #                 "Stdin_input": [],
    #                 "Filestring json": "tbd",
    #                 "Output_type": "string",
    #                 "Output_value": "Hello world"
    #             }
    #         ]
    # }

    # def to_json(self):
    #     return {
    #
    #     }
    #
    # "testcases":
    # [{
    #     "Test_id": "1",
    #     "Stdin_input": ["3", "3"],
    #     "Filestring json": "formatted string with test data input",
    #     "Output_type": "int",
    #     "Output_value": "6"
    # },
    #     {
    #         "Test_id": "2",
    #         "Stdin_input": ["5", "7"],
    #         "Filestring json": "tbd",
    #         "Output_type": "int",
    #         "Output_value": "12"
    #     }
    # ]


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

# class Student(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     tasks = models.ManyToManyField(Task)
