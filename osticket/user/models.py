import datetime
from django.db import models
from django.utils import timezone


# Create your models here.

class Users(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    status = models.IntegerField(default=0)
    created = models.DateTimeField('date created')
    def __str__(self):
        return self.username
    def was_published_recently(self):
        return self.created >= timezone.now() - datetime.timedelta(days=1)