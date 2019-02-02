from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    timeout = models.FloatField()
    solve_status = models.BooleanField()


