# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.hashers import check_password
from user.models import *

class UserUsers(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    status = models.IntegerField(default=0)
    created = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'users'



def get_user(usname):
    try:
        return UserUsers.objects.get(username=usname)
    except UserUsers.DoesNotExist:
        return None

#class SettingsBackend:
def authenticate_user(request, username, password):
    u = get_user(username)
    if u is not None:
        login_valid = (u.username == username)
        #pwd_valid = check_password(password, u.password)
        pwd_valid = (password == u.password)
        if login_valid and pwd_valid:
            return u
    else:
        return None
