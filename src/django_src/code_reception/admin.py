from django.contrib import admin
from .models import Task, TestCase, TaskResult, Course

admin.site.register(Task)
admin.site.register(TestCase)
admin.site.register(TaskResult)
admin.site.register(Course)

