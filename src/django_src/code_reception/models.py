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

    @staticmethod
    def get_all_tasks():
        return [task.title for task in Task.objects.all()]

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
    compile_result = models.TextField(max_length=1000, default="")


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
    questions_per_student = models.SmallIntegerField(default=1)

    bracket_1 =  models.ManyToManyField(Task, related_name='task_bracket_1',   blank=True)
    bracket_2 =  models.ManyToManyField(Task, related_name='task_bracket_2',   blank=True)
    bracket_3 =  models.ManyToManyField(Task, related_name='task_bracket_3',   blank=True)
    bracket_4 =  models.ManyToManyField(Task, related_name='task_bracket_4',   blank=True)
    bracket_5 =  models.ManyToManyField(Task, related_name='task_bracket_5',   blank=True)
    bracket_6 =  models.ManyToManyField(Task, related_name='task_bracket_6',   blank=True)
    bracket_7 =  models.ManyToManyField(Task, related_name='task_bracket_7',   blank=True)
    bracket_8 =  models.ManyToManyField(Task, related_name='task_bracket_8',   blank=True)
    bracket_9 =  models.ManyToManyField(Task, related_name='task_bracket_9',   blank=True)
    bracket_10 = models.ManyToManyField(Task, related_name='task_bracket_10',  blank=True)
    bracket_11 = models.ManyToManyField(Task, related_name='task_bracket_11',  blank=True)
    bracket_12 = models.ManyToManyField(Task, related_name='task_bracket_12',  blank=True)
    bracket_13 = models.ManyToManyField(Task, related_name='task_bracket_13',  blank=True)
    bracket_14 = models.ManyToManyField(Task, related_name='task_bracket_14',  blank=True)
    bracket_15 = models.ManyToManyField(Task, related_name='task_bracket_15',  blank=True)
    bracket_16 = models.ManyToManyField(Task, related_name='task_bracket_16',  blank=True)
    bracket_17 = models.ManyToManyField(Task, related_name='task_bracket_17',  blank=True)
    bracket_18 = models.ManyToManyField(Task, related_name='task_bracket_18',  blank=True)
    bracket_19 = models.ManyToManyField(Task, related_name='task_bracket_19',  blank=True)
    bracket_20 = models.ManyToManyField(Task, related_name='task_bracket_20',  blank=True)
    bracket_21 = models.ManyToManyField(Task, related_name='task_bracket_21',  blank=True)
    bracket_22 = models.ManyToManyField(Task, related_name='task_bracket_22',  blank=True)
    bracket_23 = models.ManyToManyField(Task, related_name='task_bracket_23',  blank=True)
    bracket_24 = models.ManyToManyField(Task, related_name='task_bracket_24',  blank=True)
    bracket_25 = models.ManyToManyField(Task, related_name='task_bracket_25',  blank=True)
    bracket_26 = models.ManyToManyField(Task, related_name='task_bracket_26',  blank=True)
    bracket_27 = models.ManyToManyField(Task, related_name='task_bracket_27',  blank=True)
    bracket_28 = models.ManyToManyField(Task, related_name='task_bracket_28',  blank=True)
    bracket_29 = models.ManyToManyField(Task, related_name='task_bracket_29',  blank=True)
    bracket_30 = models.ManyToManyField(Task, related_name='task_bracket_30',  blank=True)


    @staticmethod
    def bracket_list():
        return ['bracket_' + str(i) for i in range(1, 31)]

    @staticmethod
    def bracket_dict():
        return {i: 'bracket_' + str(i) for i in range(1, 31)}
    # @property
    # def brackets(self):
    #     for i in range(self.questions_per_student):
    #         setattr(self, 'bracket_' + str(i), models.ForeignKey(Task, related_name='task_bracket'))

    def __str__(self):
        def name(s):
            l = s.split()
            new = ""
            for i in range(len(l) - 1):
                s = l[i]
                new += (s[0].upper() + '.')
            new += l[-1].title()
            return new

        try:
            author = name(self.author.get_full_name())
        except AttributeError:
            author = ''
        return f"{self.name}, {author}"

class CoursesCollection(models.Model):
    courses = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)

# class StudentGroup(models.Model):
#     group_name = models.CharField(max_length=30)
    # student = models.ForeignKey(User, on_delete=models.CASCADE)
