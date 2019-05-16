from django.db import models
from django.contrib.auth.models import User


class StudentGroup(models.Model):
    group_name = models.CharField(max_length=30, default='Default_orm_group')
    students = models.ManyToManyField(User, default=None, blank=True)

    def __str__(self):
        return f'Группа: {self.group_name}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.TextField(default='Default_Group')
    #student_groups = models.ManyToManyField(StudentGroup, default=None, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile, group: {self.group}'

    # def save(self):
    #     super.save()
        # do group pre-processing?

