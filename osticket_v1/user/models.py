# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
# from django.contrib.auth.hashers import check_password
from user.models import *

class Users(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=255,null=True)
    receive_email = models.IntegerField(default=1)
    status = models.IntegerField(default=0)
    created = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'users'
    


class Topics(models.Model):
    name = models.CharField(max_length=255)
    status = models.IntegerField(default=0)
    type_send = models.IntegerField(default=1)
    description = models.TextField()


    class Meta:
        managed = True
        db_table = 'topics'


class Agents(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    phone = models.CharField(max_length=255,null=True)
    receive_email = models.IntegerField(default=1)
    password = models.CharField(max_length=255)
    admin = models.IntegerField(default=0)
    status = models.IntegerField(default=1)

    class Meta:
        managed = True
        db_table = 'agents'


class Tickets(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    sender = models.ForeignKey('Users', models.CASCADE, db_column='sender')
    topicid = models.ForeignKey('Topics', models.DO_NOTHING, db_column='topicid')
    status = models.IntegerField(default=0)
    datestart = models.DateTimeField()
    dateend = models.DateTimeField()
    attach = models.FileField(null=True, blank=True, upload_to='photos')
    class Meta:
        managed = True
        db_table = 'tickets'



class TicketAgent(models.Model):
    agentid = models.ForeignKey(Agents, models.CASCADE, db_column='agentid')
    ticketid = models.ForeignKey(Tickets, models.CASCADE, db_column='ticketid')

    class Meta:
        managed = True
        db_table = 'ticket_agent'


class ForwardTickets(models.Model):
    senderid = models.ForeignKey(Agents, models.CASCADE, db_column='senderid', related_name='sender')
    receiverid = models.ForeignKey(Agents, models.CASCADE, db_column='receiverid', related_name='receiver')
    ticketid = models.ForeignKey(Tickets, models.CASCADE, db_column='ticketid')
    content = models.TextField()

    class Meta:
        managed = True
        db_table = 'forward_tickets'


class AddAgents(models.Model):
    senderid = models.ForeignKey(Agents, models.CASCADE, db_column='senderid', related_name='senderadd')
    receiverid = models.ForeignKey(Agents, models.CASCADE, db_column='receiverid', related_name='receiveradd')
    ticketid = models.ForeignKey(Tickets, models.CASCADE, db_column='ticketid')
    content = models.TextField()

    class Meta:
        managed = True
        db_table = 'add_agents'


class Comments(models.Model):
    userid = models.ForeignKey(Users, models.CASCADE, null=True, db_column='userid', related_name='usercm')
    agentid = models.ForeignKey(Agents, models.CASCADE, null=True, db_column='agentid', related_name='agentcm')
    ticketid = models.ForeignKey(Tickets, models.CASCADE, db_column='ticketid', related_name='ticketcm')
    content = models.TextField()
    date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'comments'


def get_user(usname):
    try:
        return Users.objects.get(username=usname)
    except Users.DoesNotExist:
        return None


def get_agent(agentname):
    try:
        return Agents.objects.get(username=agentname)
    except Agents.DoesNotExist:
        return None


def get_user_email(email1):
    try:
        return Users.objects.get(email=email1)
    except Users.DoesNotExist:
        return None


def active(user):
        if user.status == 0:
            return False
        else:
            return True

def authenticate_user(username, password):
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
    else:
        return None


def authenticate_agent(agentname, agentpass):
    u = get_agent(agentname)
    if u is not None:
        login_valid = (u.username == agentname)
        #pwd_valid = check_password(password, u.password)
        pwd_valid = (agentpass == u.password)
        admin_valid = u.admin
        status_valid = u.status
        if login_valid and pwd_valid and status_valid:
            if admin_valid:
                return 1
            else:
                return 0
        else:
            return None
    else:
        return None