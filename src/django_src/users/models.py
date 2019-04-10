from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.TextField(default='Default_Group')

    def __str__(self):
        return f'{self.user.username} Profile, group: {self.group}'

    # def save(self):
    #     super.save()
        # do group pre-processing?
