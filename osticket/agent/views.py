from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone

from user.models import *
from .forms import ForwardForm, AddForm
from django.core.mail import EmailMessage
import simplejson as json
from django.utils.safestring import mark_safe
import json
import string
import os
from datetime import datetime
from datetime import timedelta
min_char = 8
max_char = 12
allchar = string.ascii_letters + string.digits


# Create your views here.
def home_admin(request):
    if request.session.has_key('admin'):
        admin = Agents.objects.get(username=request.session['admin'])
        agent = Agents.objects.exclude(username=request.session['admin'])
        agent_total = Agents.objects.count()
        tk_processing = Tickets.objects.filter(Q(status=1) | Q(status=2)).count()
        tk_done = Tickets.objects.filter(status=3).count()
        tk_open = Tickets.objects.filter(status=0).count()
        list_other = {}
        tk = Tickets.objects.all()
        for tk in tk:
            list_other[tk.id] = list_hd(tk.id)
        content = {'ticket': Tickets.objects.all(),
                   'handler': TicketAgent.objects.all(),
                   'admin': admin,
                   'list_other': list_other.items(),
                   'today': timezone.now().date(),
                   'agent': agent,
                   'agent_name': mark_safe(json.dumps(admin.username)),
                   'fullname': mark_safe(json.dumps(admin.fullname)),
                   'agent_total': agent_total,
                   'tk_open': tk_open,
                   'tk_processing': tk_processing,
                   'tk_done': tk_done}
        if request.method == 'POST':
            if 'close' in request.POST:
                ticketid = request.POST['close']
                tk = Tickets.objects.get(id=ticketid)
                if tk.status == 3:
                    if not TicketAgent.objects.filter(ticketid=tk):
                        tk.status = 0
                        action = "re-open ticket"
                    else:
                        tk.status = 1
                        action = "re-process ticket"
                else:
                    tk.status = 3
                    action = "close ticket"
                tk.save()
                TicketLog.objects.create(agentid=admin, ticketid=tk,
                                         action=action,
                                         date=timezone.now().date(),
                                         time=timezone.now().time())
            elif 'delete' in request.POST:
                ticketid = request.POST['delete']
                tk = Tickets.objects.get(id=ticketid)
                tk.delete()
                try:
                    os.remove(r'notification/chat/chat_'+ticketid+'.txt')
                except:
                    pass
            elif 'ticketid' in request.POST:
                list_agent = request.POST['list_agent[]']
                list_agent = json.loads(list_agent)
                ticketid = request.POST['ticketid']
                if not list_agent:
                    try:
                        tk = Tickets.objects.get(id=ticketid)
                        tkag1 = TicketAgent.objects.filter(ticketid=tk)
                        tkag1.delete()
                        tk.status = 0
                        tk.save()
                        action = "received ticket forward from (admin)" + admin.fullname
                        tklog = TicketLog.objects.filter(action=action)
                        tklog.delete()
                    except:
                        tk.status = 0
                        tk.save()
                else:
                    try:
                        tk = Tickets.objects.get(id=ticketid)
                        tkag1 = TicketAgent.objects.filter(ticketid=tk)
                        tkag1.delete()
                        action = "received ticket forward from (admin)" + admin.fullname
                        tklog = TicketLog.objects.filter(action=action)
                        tklog.delete()
                    except:
                        pass
                    for agentid in list_agent:
                        agent = Agents.objects.get(username=agentid)
                        tk = Tickets.objects.get(id=ticketid)
                        tkag = TicketAgent(agentid=agent, ticketid=tk)
                        tkag.save()
                        tk.status = 1
                        tk.save()
                        action = "received ticket forward from (admin)" + admin.fullname
                        if agent.receive_email == 1:
                            email = EmailMessage(
                                'Forward ticket',
                                render_to_string('agent/mail/forward_mail_leader.html',
                                                 {'receiver': agent,
                                                #   'domain': (get_current_site(request)).domain,
                                                  'domain': "113.190.232.90:8892",
                                                  'sender': 'Leader'}),
                                to=[agent.email],
                            )
                            email.send()
                        TicketLog.objects.create(agentid=agent, ticketid=tk,
                                                 action=action,
                                                 date=timezone.now().date(),
                                                 time=timezone.now().time())
            
        return render(request, 'agent/home_admin.html', content)
    else:
        return redirect('/')


def manager_topic(request):
    if request.session.has_key('admin'):
        admin = Agents.objects.get(username=request.session['admin'])
        content = {'topic': Topics.objects.all(), 'admin': admin,'today': timezone.now().date(), 'agent_name': mark_safe(json.dumps(admin.username)),
                   'fullname': mark_safe(json.dumps(admin.fullname))}
        if request.method == 'POST':
            if 'close' in request.POST:
                topictid = request.POST['close']
                tp = Topics.objects.get(id=topictid)
                if tp.status == 0:
                    tp.status = 1
                else:
                    tp.status = 0
                tp.save()
            elif 'delete' in request.POST:
                topictid = request.POST['delete']
                tp = Topics.objects.get(id=topictid)
                tk = Tickets.objects.filter(topicid=tp)
                tp_other = Topics.objects.get(name='Other')
                for ticket in tk:
                    ticket.topicid = tp_other
                    ticket.save()
                tp.delete()
            elif 'add_topic' in request.POST:
                if request.POST['topicid'] == '0':
                    topicname = request.POST['add_topic']
                    description = request.POST['description']
                    type_send = request.POST['type_send']
                    tp = Topics(name=topicname, description=description, type_send=type_send)
                    tp.save()
                else:
                    tp = Topics.objects.get(id=request.POST['topicid'])
                    tp.name = request.POST['add_topic']
                    tp.description = request.POST['description']
                    tp.type_send = request.POST['type_send']
                    tp.save()
        return render(request, 'agent/manager_topic.html', content)
    else:
        return redirect('/')


def manager_agent(request):
    if request.session.has_key('admin'):
        admin = Agents.objects.get(username=request.session['admin'])
        list_tk = {}
        ag = Agents.objects.all()
        for ag in ag:
            list_tk[ag.username] = count_tk(ag.username)
        content = {'agent': Agents.objects.all(),
                   'admin': admin,
                   'list_tk': list_tk.items(),
                   'today': timezone.now().date(),
                   'agent_name': mark_safe(json.dumps(admin.username)),
                   'fullname': mark_safe(json.dumps(admin.fullname))}
        if request.method == 'POST':
            if 'close' in request.POST:
                agentid = request.POST['close']
                ag = Agents.objects.get(id=agentid)
                if ag.status == 0:
                    ag.status = 1
                else:
                    ag.status = 0
                ag.save()
            elif 'delete' in request.POST:
                agentid = request.POST['delete']
                ag = Agents.objects.get(id=agentid)
                ag.delete()
            elif 'add_agent' in request.POST:
                if request.POST['agentid'] == '0':
                    fullname = request.POST['add_agent']
                    email = request.POST['email']
                    phone = request.POST['phone']
                    username = request.POST['username']
                    password = request.POST['password']
                    ag = Agents(fullname=fullname, username=username, phone=phone, email=email, password=password)
                    ag.save()
                else:
                    ag = Agents.objects.get(id=request.POST['agentid'])
                    fullname = request.POST['add_agent']
                    email = request.POST['email']
                    phone = request.POST['phone']
                    ag.fullname = fullname
                    ag.email = email
                    ag.phone = phone
                    ag.save()
                    username = ag.username
        return render(request, 'agent/manager_agent.html', content)
    else:
        return redirect('/')


def logout_admin(request):
    del request.session['admin']
    return redirect("/")


def logout(request):
    del request.session['agent']
    return redirect("/")


def home_agent(request):
    if request.session.has_key('agent')and(Agents.objects.get(username=request.session['agent'])).status == 1:
        agent = Agents.objects.get(username=request.session.get('agent'))
        topic = Topics.objects.exclude(Q(name='Other') | Q(type_send=0))
        user_total = Users.objects.count()
        process = Tickets.objects.filter(Q(status=1) | Q(status=2))
        done = Tickets.objects.filter(status=3)
        tk_open = Tickets.objects.filter(status=0, topicid__in=topic).count()
        tk_processing = TicketAgent.objects.filter(agentid=agent, ticketid__in=process).count()
        tk_done = TicketAgent.objects.filter(agentid=agent, ticketid__in=done).count()
        content = {'ticket': Tickets.objects.filter(status=0, topicid__in=topic).order_by('datestart'),
                    'agent': agent, 'agent_name': mark_safe(json.dumps(agent.username)),
                    'fullname': mark_safe(json.dumps(agent.fullname)),
                    'user_total': user_total,
                    'tk_open': tk_open,
                    'tk_processing': tk_processing,
                    'tk_done': tk_done,
                    'noti_noti': agent.noti_noti,
                    'noti_chat': agent.noti_chat}
        if request.method == 'POST':
            if 'tkid' in request.POST:
                ticket = Tickets.objects.get(id=request.POST['tkid'])
                ticket.status = 1
                ticket.save()
                TicketLog.objects.create(agentid=agent, ticketid=ticket, action='assign ticket',
                                         date=timezone.now().date(),
                                         time=timezone.now().time())
                TicketAgent.objects.create(agentid=agent, ticketid=ticket)
                user = Users.objects.get(id=ticket.sender.id)
                # if user.receive_email == 1:
                #     email = EmailMessage(
                #         'Assign ticket',
                #         render_to_string('agent/mail/assign_mail.html',
                #                          {'receiver': user,
                #                           'domain': (get_current_site(request)).domain,
                #                           'sender': agent,
                #                           'ticketid': ticket.id}),
                #         to=[user.email],
                #     )
                #     email.send()
            if 'noti_noti' in request.POST:
                agent.noti_noti = 0
                agent.save()
            if 'noti_chat' in request.POST:
                agent.noti_chat = 0
                agent.save()
            # if 'date' in request.POST:
            #     date1 = request.POST['date']
            #     dtDate = datetime.strptime(date1, "%Y-%m-%d").date() + timedelta(days=1)
            #     end = dtDate + timedelta(days=1)
            #     tk_by_date = Tickets.objects.filter(datestart__range=[dtDate, end], ticketagent__agentid=agent)
            #     return render(request, 'agent/home_agent.html', {'tk_date': tk_by_date})
            #     print(tk_by_date)
        return render(request, 'agent/home_agent.html', content)
    else:
        return redirect("/")


def assign_ticket(request, id):
    if request.session.has_key('agent')and(Agents.objects.get(username=request.session['agent'])).status == 1:
        ticket = Tickets.objects.get(id=id)
        agent = Agents.objects.get(username=request.session['agent'])
        ticket.status = 1
        ticket.save()
        TicketLog.objects.create(agentid=agent, ticketid=ticket, action='assign ticket',
                                 date=timezone.now().date(),
                                 time=timezone.now().time())
        TicketAgent.objects.create(agentid=agent, ticketid=ticket)
        user = Users.objects.get(id=ticket.sender.id)
        if user.receive_email == 1:
            email = EmailMessage(
                'Assign ticket',
                render_to_string('agent/mail/assign_mail.html',
                                 {'receiver': user,
                                 'domain': "113.190.232.90:8892",
                                #   'domain': (get_current_site(request)).domain,
                                  'sender': agent,
                                  'ticketid': ticket.id}),
                to=[user.email],
            )
            email.send()
        return redirect("/agent")
    else:
        return redirect("/")


def processing_ticket(request):
    if request.session.has_key('agent')and(Agents.objects.get(username=request.session['agent'])).status == 1:
        agent = Agents.objects.exclude(Q(username=request.session['agent']) | Q(admin=1))
        form = ForwardForm()
        form1 = AddForm()
        sender = Agents.objects.get(username=request.session['agent'])
        tksd = TicketAgent.objects.filter(agentid=sender)
        tksdpr = Tickets.objects.filter(id__in=tksd.values('ticketid'),status__in=[1, 2])
        agk = {}
        agc = {}
        gua = {}
        for tk in tksdpr:
            agt = TicketAgent.objects.filter(ticketid=tk).values('agentid')
            tem = [x.username for x in Agents.objects.filter(id__in=agt, admin=0)]
            if len(tem) > 1:
                gua[tk.id] = 'yes'
            else:
                gua[tk.id] = 'no'
            agc[tk.id] = tem
        content = {'noti_noti': sender.noti_noti,
                    'noti_chat': sender.noti_chat, 'agent': agent, 'ticket': tksdpr, 'agc': agc, 'form': form, 'form1': form1, 'gua': gua, 'agent_name': mark_safe(json.dumps(sender.username)), 'fullname': mark_safe(json.dumps(sender.fullname))}
        if request.method == 'POST':
            if 'noti_noti' in request.POST:
                sender.noti_noti = 0
                sender.save()
            elif 'noti_chat' in request.POST:
                sender.noti_chat = 0
                sender.save()
            elif 'type' in request.POST:
                if request.POST['type'] == 'forward_agent':
                    list_agent = request.POST['list_agent[]']
                    list_agent = json.loads(list_agent)
                    tk = Tickets.objects.get(id=request.POST['ticketid'])
                    receiver = Agents.objects.filter(username__in=list_agent)
                    text = request.POST['content']
                    for rc in receiver:
                        if rc != sender:
                            try:
                                TicketAgent.objects.get(ticketid=tk, agentid=rc)
                            except ObjectDoesNotExist:
                                try:
                                    ForwardTickets.objects.get(senderid=sender, receiverid=rc, ticketid=tk)
                                except ObjectDoesNotExist:
                                    ForwardTickets.objects.create(senderid=sender, receiverid=rc, ticketid=tk,content=text)
                                    if rc.receive_email == 1:
                                        email = EmailMessage(
                                            'Forward ticket',
                                            render_to_string('agent/mail/forward_mail.html',
                                                            {'receiver': rc,
                                                            'domain': "113.190.232.90:8892",
                                                            # 'domain': (get_current_site(request)).domain,
                                                            'sender': sender}),
                                            to=[rc.email],
                                        )
                                        email.send()
                    return redirect("/agent/processing_ticket")
                elif request.POST['type'] == 'add_agent':
                    list_agent = request.POST['list_agent[]']
                    list_agent = json.loads(list_agent)
                    tk = Tickets.objects.get(id=request.POST['ticketid'])
                    receiver = Agents.objects.filter(username__in=list_agent)
                    text = request.POST['content']
                    for rc in receiver:
                        if rc != sender:
                            try:
                                TicketAgent.objects.get(ticketid=tk,agentid=rc)
                            except ObjectDoesNotExist:
                                try:
                                    AddAgents.objects.get(senderid=sender, receiverid=rc, ticketid=tk)
                                except ObjectDoesNotExist:
                                    AddAgents.objects.create(senderid=sender, receiverid=rc, ticketid=tk, content=text)
                                    if rc.receive_email == 1:
                                        email = EmailMessage(
                                            'Add in a ticket',
                                            render_to_string('agent/mail/add_mail.html',
                                                            {'receiver': rc,
                                                            'domain': "113.190.232.90:8892",
                                                            # 'domain': (get_current_site(request)).domain,
                                                            'sender': sender}),
                                            to=[rc.email]
                                        )
                                        email.send()
                    return redirect("/agent/processing_ticket")
                elif request.POST['type'] == 'process_done':
                    tkid = request.POST['tkid']
                    stt = request.POST['stt']
                    ticket = Tickets.objects.get(id=tkid)
                    ticket.status = stt
                    ticket.save()
                    if stt == 1:
                        action = 're-process ticket'
                    else:
                        action = 'done ticket'
                        user = Users.objects.get(id=ticket.sender.id)
                        # if user.receive_email == 1:
                        #     email = EmailMessage(
                        #         'Finished ticket',
                        #         render_to_string('agent/mail/done_mail.html',
                        #                         {'receiver': user,
                        #                         'domain': (get_current_site(request)).domain,
                        #                         'sender': sender,
                        #                         'ticketid': ticket.id}),
                        #         to=[user.email],
                        #     )
                        #     email.send()
                    TicketLog.objects.create(agentid=sender, ticketid=ticket,
                                            action=action,
                                            date=timezone.now().date(),
                                            time=timezone.now().time())
                elif request.POST['type'] == 'give_up':
                    ticket = Tickets.objects.get(id=request.POST['tkid'])
                    try:
                        TicketAgent.objects.get(ticketid=ticket)
                    except MultipleObjectsReturned:
                        tk = TicketAgent.objects.get(ticketid=ticket, agentid=sender)
                        tk.delete()
                        TicketLog.objects.create(agentid=sender, ticketid=ticket, action='give up ticket',
                                                date=timezone.now().date(),
                                                time=timezone.now().time())
        return render(request, 'agent/processing_ticket.html', content)
    else:
        return redirect("/")


def history(request,id):
    if (request.session.has_key('agent')and(Agents.objects.get(username=request.session['agent'])).status == 1) or request.session.has_key('admin'):
        tems = TicketLog.objects.filter(ticketid=id)
        result = []
        for tem in tems:
            if tem.userid is not None:
                action = "<b>User " + str(tem.userid.fullname) + "</b><br/>"+str(tem.action)
            else:
                action = "<b>Agent " + str(tem.agentid.fullname) + "</b><br/>"+str(tem.action)
            if tem.action == 'create ticket':
                cont = "<i class='fa fa-plus' ></i>"
            elif tem.action == 'close ticket':
                cont = "<i class='fa fa-power-off' ></i>"
            elif tem.action == 'assign ticket':
                cont = "<i class='fa fa-thumb-tack' ></i>"
            elif tem.action == 'done ticket':
                cont = "<i class='fa fa-check' ></i>"
            elif tem.action == 're-process ticket':
                cont = "<i class='fa fa-refresh' ></i>"
            elif tem.action == 're-open ticket':
                cont = "<i class='fa fa-repeat' ></i>"
            elif tem.action == 'give up ticket':
                cont = "<i class='fa fa-sign-out' ></i>"
            else:
                cont = "<i class='fa fa-user-secret'></i>"
            result.append({"id": tem.id,
                           "title": action,
                           "content": cont,
                           "group": "period",
                           "start": str(tem.date)+"T"+str(tem.time)[:-7]})
        maxtime = TicketLog.objects.filter(ticketid=id).latest('id')
        mintime = TicketLog.objects.filter(ticketid=id).earliest('id')
        if maxtime.ticketid.status == 0:
            status = '<font color="red">pending</font>'
        elif maxtime.ticketid.status == 1:
            status = '<font color="orange">processing</font>'
        elif maxtime.ticketid.status == 2:
            status = '<font color="green">done</font>'
        else:
            status = '<font color="gray">close</font>'
        tim = str(timezone.datetime.combine(maxtime.date, maxtime.time) - timezone.datetime.combine(
            mintime.date, mintime.time))[:-7]
        result.append({"id": 0,
                       "content": "Ticket no."+str(id)+" " + status + " (exist time " + tim + ")",
                       "type": "point",
                       "group": "overview",
                       "start": str(mintime.date) + "T" + str(mintime.time)[:-7]})
        tk = json.loads(json.dumps(result))
        if request.session.has_key('agent'):
            return render(request, 'agent/history_for_agent.html', {'tk': tk, 'id': str(id)})
        else:
            return render(request, 'agent/history_for_admin.html', {'tk': tk, 'id': str(id), 'today': timezone.now().date()})
    else:
        return redirect("/")


def history_all_ticket(request, date, date2):
    if request.session.has_key('admin'):
        admin = Agents.objects.get(admin=1)
        # time = timezone.now().time()
        tdate1 = timezone.datetime.strptime(date, "%Y-%m-%d").date()
        tdate2 = timezone.datetime.strptime(date2, "%Y-%m-%d").date()
        # nday = str(timezone.datetime.combine(tdate2, time) - timezone.datetime.combine(tdate1, time))[:-13]
        # if nday == '':
        #     nday = 1
        # else:
        #     nday = int(nday)+1
        # tickets = {}
        tickets = TicketLog.objects.filter(date__range=[tdate1, tdate2])
        # for x in range(0, nday):
        #     thisDate = str(tdate2-timezone.timedelta(days=x))
        #     tk = TicketLog.objects.filter(date=thisDate).order_by('id').reverse()
        #     if tk:
        #         tickets[thisDate] = tk
        return render(request, 'agent/history_all_ticket.html', {'tickets': tickets, 'today': timezone.now().date(),
                                                                 'day1': tdate1,
                                                                 'day2': date2,
                                                                 'agent_name': mark_safe(json.dumps(admin.username)),
                                                                 'fullname': mark_safe(json.dumps(admin.fullname))})
    else:
        return redirect("/")


def inbox(request):
    if request.session.has_key('agent')and(Agents.objects.get(username=request.session['agent'])).status == 1:
        agent = Agents.objects.get(username=request.session.get('agent'))
        content = {'forwardin': ForwardTickets.objects.filter(receiverid=agent),
                    'noti_noti': agent.noti_noti,
                    'noti_chat': agent.noti_chat,
                   'addin': AddAgents.objects.filter(receiverid=agent), 'agent_name': mark_safe(json.dumps(agent.username)), 'fullname': mark_safe(json.dumps(agent.fullname))}
        if request.method == 'POST':
            
            if 'forward' in request.POST:
                ticket = Tickets.objects.get(id=request.POST['tkid'])
                try:
                    addagent = AddAgents.objects.get(ticketid=ticket, receiverid=agent)
                except ObjectDoesNotExist:
                    pass
                else:
                    addagent.delete()
                fwticket = ForwardTickets.objects.get(ticketid=ticket, receiverid=agent)
                sender = fwticket.senderid
                agticket = TicketAgent.objects.get(ticketid=ticket, agentid=fwticket.senderid)
                fwticket.delete()
                if 'agree' not in request.POST:
                    if sender.receive_email == 1:
                        email = EmailMessage(
                            'Deny forward request',
                            render_to_string('agent/mail/deny_mail.html',
                                             {'receiver': sender,
                                             'domain': "113.190.232.90:8892",
                                            #   'domain': (get_current_site(request)).domain,
                                              'sender': agent}),
                            to=[sender.email]
                        )
                        email.send()
                else:
                    try:
                        TicketAgent.objects.get(ticketid=ticket, agentid=agent)
                    except TicketAgent.DoesNotExist:
                        agticket.agentid = agent
                        agticket.save()
                        action = "received ticket forward from (agent)" + sender.fullname
                        TicketLog.objects.create(agentid=agent, ticketid=ticket, action=action,
                                                 date=timezone.now().date(),
                                                 time=timezone.now().time())
                        if sender.receive_email == 1:
                            email = EmailMessage(
                                'Accept forward request',
                                render_to_string('agent/mail/accept_mail.html',
                                                 {'receiver': sender,
                                                 'domain': "113.190.232.90:8892",
                                                #   'domain': (get_current_site(request)).domain,
                                                  'sender': agent}),
                                to=[sender.email]
                            )
                            email.send()
                    else:
                        agticket.delete()
            elif 'add' in request.POST:
                ticket = Tickets.objects.get(id=request.POST['tkid'])
                try:
                    fwticket = ForwardTickets.objects.get(ticketid=ticket, receiverid=agent)
                except ObjectDoesNotExist:
                    pass
                else:
                    fwticket.delete()
                addagent = AddAgents.objects.get(ticketid=ticket, receiverid=agent)
                sender = addagent.senderid
                addagent.delete()
                if 'agree' not in request.POST:
                    if sender.receive_email == 1:
                        email = EmailMessage(
                            'Deny add request',
                            render_to_string('agent/mail/deny_mail.html',
                                             {'receiver': sender,
                                             'domain': "113.190.232.90:8892",
                                            #   'domain': (get_current_site(request)).domain,
                                              'sender': agent}),
                            to=[sender.email]
                        )
                        email.send()
                else:
                    try:
                        TicketAgent.objects.get(ticketid=ticket, agentid=agent)
                    except TicketAgent.DoesNotExist:
                        TicketAgent.objects.create(ticketid=ticket, agentid=agent)
                        action = 'join to handler ticket'
                        TicketLog.objects.create(agentid=agent, ticketid=ticket, action=action,
                                                 date=timezone.now().date(),
                                                 time=timezone.now().time())
                        if sender.receive_email == 1:
                            email = EmailMessage(
                                'Accept add request',
                                render_to_string('agent/mail/accept_mail.html',
                                                 {'receiver': sender,
                                                 'domain': "113.190.232.90:8892",
                                                #   'domain': (get_current_site(request)).domain,
                                                  'sender': agent}),
                                to=[sender.email]
                            )
                            email.send()
            elif 'noti_noti' in request.POST:
                agent.noti_noti = 0
                agent.save()
            elif 'noti_chat' in request.POST:
                agent.noti_chat = 0
                agent.save()
        return render(request, 'agent/inbox.html', content)
    else:
        return redirect("/")




def outbox(request):
    if request.session.has_key('agent')and(Agents.objects.get(username=request.session['agent'])).status == 1:
        agent = Agents.objects.get(username=request.session.get('agent'))
        content ={'forwardout':ForwardTickets.objects.filter(senderid=agent),
                    'noti_noti': agent.noti_noti,
                    'noti_chat': agent.noti_chat,
                  'addout': AddAgents.objects.filter(senderid=agent), 'agent_name': mark_safe(json.dumps(agent.username)), 'fullname': mark_safe(json.dumps(agent.fullname))}
        if request.method == 'POST':
            if 'forward' in request.POST:
                fwticket = ForwardTickets.objects.get(id=request.POST['tkid'])
            elif 'add' in request.POST:
                fwticket = AddAgents.objects.get(id=request.POST['tkid'])
            elif 'noti_noti' in request.POST:
                agent.noti_noti = 0
                agent.save()
            elif 'noti_chat' in request.POST:
                agent.noti_chat = 0
                agent.save()
            fwticket.delete()
        return render(request,'agent/outbox.html',content)
    else:
        return redirect("/")


def profile(request):
    if request.session.has_key('agent')and(Agents.objects.get(username=request.session['agent'])).status == 1:
        agent = Agents.objects.get(username=request.session['agent'])
        if request.method == 'POST':
            if 'change_user' in request.POST:
                u = Agents.objects.get(id=request.POST['agentid'])
                fullname = request.POST['change_user']
                email = request.POST['email']
                phone = request.POST['phone']
                receive_mail = request.POST['receive_mail']
                u.fullname = fullname
                u.email = email
                u.phone = phone
                u.receive_email = receive_mail
                u.save()
            elif 'pwd' in request.POST:
                u = Agents.objects.get(id=request.POST['agentid'])
                u.password = request.POST['pwd']
                u.save()
            elif 'noti_noti' in request.POST:
                agent.noti_noti = 0
                agent.save()
            elif 'noti_chat' in request.POST:
                agent.noti_chat = 0
                agent.save()
        return render(request,"agent/profile.html",{'agent':agent, 'noti_noti': agent.noti_noti,
                    'noti_chat': agent.noti_chat, 'agent_name': mark_safe(json.dumps(agent.username)), 'fullname': mark_safe(json.dumps(agent.fullname))})
    else:
        return redirect("/")


def closed_ticket(request):
    if request.session.has_key('agent')and(Agents.objects.get(username=request.session['agent'])).status == 1:
        agent = Agents.objects.get(username=request.session['agent'])
        tem = Tickets.objects.filter(status=3)
        content = {'noti_noti': agent.noti_noti,
                    'noti_chat': agent.noti_chat, 'ticket': TicketAgent.objects.filter(agentid=agent, ticketid__in=tem), 'agent_name': mark_safe(json.dumps(agent.username)), 'fullname': mark_safe(json.dumps(agent.fullname))}
        if request.method == 'POST':
            if 'noti_noti' in request.POST:
                agent.noti_noti = 0
                agent.save()
            elif 'noti_chat' in request.POST:
                agent.noti_chat = 0
                agent.save()
        return render(request,'agent/closed_ticket.html', content)
    else:
        return redirect("/")


def manager_user(request):
    if request.session.has_key('agent')and(Agents.objects.get(username=request.session['agent'])).status == 1:
        agent = Agents.objects.get(username=request.session['agent'])
        users = Users.objects.all()
        if request.method == 'POST':
            if 'noti_noti' in request.POST:
                agent.noti_noti = 0
                agent.save()
            elif 'noti_chat' in request.POST:
                agent.noti_chat = 0
                agent.save()
            else:
                user = Users.objects.get(id=request.POST['tkid'])
                user.status = request.POST['stt']
                user.save()
        
        return render(request,"agent/manage_user.html",{'noti_noti': agent.noti_noti,
                    'noti_chat': agent.noti_chat, 'user':users, 'agent_name': mark_safe(json.dumps(agent.username)), 'fullname': mark_safe(json.dumps(agent.fullname))})
    else:
        return redirect("/")





