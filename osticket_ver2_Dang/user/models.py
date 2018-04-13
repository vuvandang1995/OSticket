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

class Users(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    status = models.IntegerField(default=0)
    created = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'users'
    


class Topics(models.Model):
    name = models.CharField(max_length=255)
    status = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'topics'


class Agents(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    admin = models.IntegerField(default=0)
    leader = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'agents'

class Tickets(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    sender = models.ForeignKey('Users', models.DO_NOTHING, db_column='sender')
    topicid = models.ForeignKey('Topics', models.DO_NOTHING, db_column='topicid')
    status = models.IntegerField(default=0)
    datestart = models.DateTimeField()
    dateend = models.DateTimeField()
    attach = models.ImageField(upload_to='photos')
    class Meta:
        managed = True
        db_table = 'tickets'



class TicketAgent(models.Model):
    agentid = models.ForeignKey(Agents, models.DO_NOTHING, db_column='agentid')
    ticketid = models.ForeignKey(Tickets, models.DO_NOTHING, db_column='ticketid')

    class Meta:
        managed = True
        db_table = 'ticket_agent'

def get_user(usname):
    try:
        return Users.objects.get(username=usname)
    except Users.DoesNotExist:
        return None

def active(user):
        if user.status == 0:
            return False
        else:
            return True

#class SettingsBackend:
def authenticate_user(request, username, password):
    u = get_user(username)
    if u is not None:
        login_valid = (u.username == username)
        #pwd_valid = check_password(password, u.password)
        pwd_valid = (password == u.password)
        status_valid = u.status
        if login_valid and pwd_valid and status_valid:
            return u
    else:
        return None
