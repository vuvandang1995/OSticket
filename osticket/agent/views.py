from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone

from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse

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
        # tpag = TopicAgent.objects.filter(agentid=sender).values('topicid')
        tp = Topics.objects.all()
        list_ag = {}
        for t in tp:
            ag = TopicAgent.objects.filter(topicid=t, agentid__in=agent)
            list_ag[t.name] = [a.agentid for a in ag]
        content = {'ticket': Tickets.objects.filter().order_by("-id"),
                   'list_ag': list_ag,
                   'topic': tp,
                   'handler': TicketAgent.objects.all(),
                   'admin': admin,
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
                        action = "received ticket forward from (admin)" + admin.username
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
                        action = "received ticket forward from (admin)" + admin.username
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
                        action = "received ticket forward from (admin)" + admin.username
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


def home_admin_data(request):
    if request.session.has_key('admin'):
        tk = Tickets.objects.filter().order_by("-id")
        data = []
        for tk in tk:
            if tk.status == 0:
                status = r'<span class ="label label-danger" id="leader'+str(tk.id)+'">pending</span>'
                handler = '<p id="hd' + str(tk.id) + '">Nobody</p>'
            else:
                if tk.status == 1:
                    status = r'<span class ="label label-warning" id="leader'+str(tk.id)+'">processing</span>'
                elif tk.status == 2:
                    status = r'<span class ="label label-success" id="leader'+str(tk.id)+'">done</span>'
                else:
                    status = r'<span class ="label label-default" id="leader'+str(tk.id)+'">closed</span>'
                handler = '<p id="hd' + str(tk.id) + '">'
                for t in TicketAgent.objects.filter(ticketid=tk.id):
                    handler += t.agentid.username + "<br>"
                handler += '</p>'
            id = r'''<button type="button" class="btn" data-toggle="modal" data-target="#'''+str(tk.id)+'''content">'''+str(tk.id)+'''</button>'''
            sender = '<p id="sender' + str(tk.id) + '">' + tk.sender.username + '</p>'
            topic = '<p id="tp' + str(tk.id) + '">' + tk.topicid.name + '</p>'
            option = r'''<button type="button" class="btn btn-primary" id="'''+str(tk.id)+'''" data-toggle="tooltip" title="open/close"><i class="fa fa-power-off"></i></button>
            <button type="button" class="btn btn-danger" id="'''+str(tk.id)+'''" data-toggle="tooltip" title="delete"><i class="fa fa-trash-o"></i></button>
            <button type="button" class="btn btn-info" data-title="forward" id="'''+str(tk.id)+'''"data-toggle="modal" data-target="#forward_modal"><i class="fa fa-share-square-o" data-toggle="tooltip" title="forward" ></i></button>
            <a type="button" target=_blank class="btn btn-warning" href="/agent/history/'''+str(tk.id)+ '''" data-toggle="tooltip" title="history"><i class="fa fa-history"></i></a>'''
            data.append([id, tk.title, topic, sender, status, handler, option])
        ticket = {"data": data}
        tickets = json.loads(json.dumps(ticket))
        return JsonResponse(tickets, safe=False)


def manager_topic(request):
    if request.session.has_key('admin'):
        admin = Agents.objects.get(username=request.session['admin'])
        agent = Agents.objects.exclude(username=request.session['admin'])
        department = Departments.objects.exclude(name='admin').order_by('-id')
        list_ag = {}
        dm = Departments.objects.all()
        for dm in dm:
            list_ag[dm.name] = get_list_agent(dm.name)
        list_ag_tp = {}
        tp = Topics.objects.all()
        for tp in tp:
            list_ag_tp[tp.name] = get_agent_tp(tp.name)
        content = {'topic': Topics.objects.all(), 'admin': admin, 'today': timezone.now().date(), 'agent_name': mark_safe(json.dumps(admin.username)),
                   'fullname': mark_safe(json.dumps(admin.fullname)), 'agent':agent, 'department': department, 'list_ag': list_ag.items(), 'list_ag_tp': list_ag_tp.items(),}
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
                list_agent = request.POST['list_agent[]']
                list_agent = json.loads(list_agent)
                if request.POST['topicid'] == '0':
                    print(request.POST)
                    topicname = request.POST['add_topic']
                    description = request.POST['description']
                    department = Departments.objects.get(id=request.POST['department'])
                    tp = Topics.objects.create(name=topicname, description=description, departmentid=department)
                    for ag in list_agent:
                        ag = Agents.objects.get(username=ag)
                        TopicAgent.objects.create(agentid=ag, topicid=tp)
                else:
                    tp = Topics.objects.get(id=request.POST['topicid'])
                    tp.name = request.POST['add_topic']
                    tp.description = request.POST['description']
                    tp.departmentid = Departments.objects.get(id=request.POST['department'])
                    tp.save()
                    if not list_agent:
                        try:
                            tpag = TopicAgent.objects.filter(topicid=tp)
                            tpag.delete()
                        except:
                            pass
                    else:
                        try:
                            tpag = TopicAgent.objects.filter(topicid=tp)
                            tpag.delete()
                        except:
                            pass
                        for ag in list_agent:
                            ag = Agents.objects.get(username=ag)
                            TopicAgent.objects.create(agentid=ag, topicid=tp)
        return render(request, 'agent/manager_topic.html', content)
    else:
        return redirect('/')


def manager_department(request):
    if request.session.has_key('admin'):
        admin = Agents.objects.get(username=request.session['admin'])
        department = Departments.objects.exclude(name='admin')
        list_ag = {}
        list_tp = {}
        for dp in department:
            ags = Agents.objects.filter(departmentid=dp)
            tps = Topics.objects.filter(departmentid=dp)
            list_ag[dp.id] = [ag.fullname for ag in ags]
            list_tp[dp.id] = [tp.name for tp in tps]
        content = {'list_ag': list_ag,
                   'list_tp': list_tp,
                   'admin': admin,
                   'today': timezone.now().date(),
                   'department': department}
        if request.method == 'POST':
            if 'addname' in request.POST:
                if request.POST['dmid'] == '':
                    Departments.objects.create(name=request.POST['addname'],
                                               description=request.POST['adddescription'])
                else:
                    dp = Departments.objects.get(id=request.POST['dmid'])
                    dp.name = request.POST['addname']
                    dp.description = request.POST['adddescription']
                    dp.save()
            elif 'delete' in request.POST:
                Departments.objects.filter(id=request.POST['delete']).delete()
            return redirect("/agent/department")
        else:
            return render(request, 'agent/manage_department.html', content)
    else:
        return redirect('/')


def manager_agent(request):
    if request.session.has_key('admin'):
        admin = Agents.objects.get(username=request.session['admin'])
        department = Departments.objects.filter().order_by('-id')
        list_tk = {}
        list_tp = {}
        ag = Agents.objects.all()
        for ag in ag:
            list_tk[ag.username] = count_tk(ag.username)
            tpag = TopicAgent.objects.filter(agentid=ag).values('topicid')
            list_tp[ag.username] = [tp.name for tp in Topics.objects.filter(id__in=tpag)]
        content = {'agent': Agents.objects.all(),
                   'admin': admin,
                   'list_tk': list_tk.items(),
                   'list_tp': list_tp,
                   'today': timezone.now().date(),
                   'agent_name': mark_safe(json.dumps(admin.username)),
                   'fullname': mark_safe(json.dumps(admin.fullname)),
                   'department':department}
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
                    department = Departments.objects.get(id=request.POST['department'])
                    ag = Agents.objects.create(fullname=fullname, username=username, phone=phone, email=email, password=password, departmentid=department)
                    ag.save()
                else:
                    ag = Agents.objects.get(id=request.POST['agentid'])
                    fullname = request.POST['add_agent']
                    email = request.POST['email']
                    phone = request.POST['phone']
                    department = request.POST['department']
                    ag.fullname = fullname
                    ag.email = email
                    ag.phone = phone
                    ag.departmentid = Departments.objects.get(id=department)
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
        tpag = TopicAgent.objects.filter(agentid=agent).values('topicid')
        topic = Topics.objects.filter(id__in=tpag)
        user_total = Users.objects.count()
        process = Tickets.objects.filter(topicid__in=topic, status__in=[1,2])
        done = Tickets.objects.filter(status=3)
        tk_open = Tickets.objects.filter(status=0, topicid__in=topic).count()
        tk_processing = TicketAgent.objects.filter(agentid=agent, ticketid__in=process).count()
        tk_done = TicketAgent.objects.filter(agentid=agent, ticketid__in=done).count()
        tp = TopicAgent.objects.filter(agentid=agent)
        list_tp = ""
        for tp in tp:
            list_tp += str(tp.topicid.name) + "!"
        content = {'ticket': Tickets.objects.filter(status=0, topicid__in=topic, ).order_by('-id'),
                    'agent': agent, 'agent_name': mark_safe(json.dumps(agent.username)),
                    'fullname': mark_safe(json.dumps(agent.fullname)),
                    'user_total': user_total,
                    'tk_open': tk_open,
                    'tk_processing': tk_processing,
                    'tk_done': tk_done,
                    'noti_noti': agent.noti_noti,
                    'noti_chat': agent.noti_chat,
                    'list_tp': mark_safe(json.dumps(list_tp))}
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
        sender = Agents.objects.get(username=request.session['agent'])
        agent = Agents.objects.exclude(Q(username=request.session['agent']) | Q(admin=1))
        tpag = TopicAgent.objects.filter(agentid=sender).values('topicid')
        tp = Topics.objects.filter(id__in=tpag)
        list_ag = {}
        for t in tp:
            ag = TopicAgent.objects.filter(topicid=t, agentid__in=agent)
            list_ag[t.name] = [a.agentid for a in ag]
        form = ForwardForm()
        form1 = AddForm()
        tksd = TicketAgent.objects.filter(agentid=sender)
        tksdpr = Tickets.objects.filter(id__in=tksd.values('ticketid'),status__in=[1, 2])
        topicag = TopicAgent.objects.filter(agentid=sender)
        list_tp = ""
        for tp1 in topicag:
            list_tp += str(tp1.topicid.name) + "!"
        content = {'list_ag': list_ag,
                   'topic': tp,
                   'noti_noti': sender.noti_noti,
                   'noti_chat': sender.noti_chat,
                   'agent': agent, 'ticket': tksdpr,
                   'form': form,
                   'form1': form1,
                   'agent_name': mark_safe(json.dumps(sender.username)),
                   'fullname': mark_safe(json.dumps(sender.fullname)),
                   'list_tp': mark_safe(json.dumps(list_tp))}
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
                                    # if rc.receive_email == 1:
                                    #     email = EmailMessage(
                                    #         'Forward ticket',
                                    #         render_to_string('agent/mail/forward_mail.html',
                                    #                         {'receiver': rc,
                                    #                         'domain': "113.190.232.90:8892",
                                    #                         # 'domain': (get_current_site(request)).domain,
                                    #                         'sender': sender}),
                                    #         to=[rc.email],
                                    #     )
                                    #     email.send()
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


def processing_ticket_data(request):
    if request.session.has_key('agent')and(Agents.objects.get(username=request.session['agent'])).status == 1:
        agent = Agents.objects.get(username=request.session['agent'])
        tksd = TicketAgent.objects.filter(agentid=agent)
        tksdpr = Tickets.objects.filter(id__in=tksd.values('ticketid'), status__in=[1, 2])
        data = []
        for tk in tksdpr:
            option = ''
            if tk.status == 1:
                status = r'<span class ="label label-warning" > Processing</span>'
                option += r'''<button id="''' + str(tk.id) + '''" type="button" class="btn btn-success handle_done" data-toggle="tooltip" title="done" ><i class="fa fa-check"></i></button>'''
            else:
                status = r'<span class ="label label-success" > Done</span>'
                option += r'''<button id="''' + str(tk.id) + '''" type="button" class="btn btn-success handle_processing" data-toggle="tooltip" title="process" ><i class="fa fa-wrench"></i></button>'''
            id = r'''<th scope="row"><button type="button" class="btn" data-toggle="modal" data-target="#''' + str(tk.id) + '''content">''' + str(tk.id) + '''</button></th>'''
            handler = '<p id="hd' + str(tk.id) + '">'
            topic = '<p id="tp' + str(tk.id) + '">' + tk.topicid.name + '</p>'
            tem = 0
            for t in TicketAgent.objects.filter(ticketid=tk.id):
                tem += 1
                handler += t.agentid.username + "<br>"
            handler += '</p>'
            option += r'''<input type="hidden" id="user''' + str(tk.id) + '''" value="'''+tk.sender.username+'''">
            <a href='javascript:register_popup_agent("chat''' + str(tk.id) + '''", ''' + str(tk.id) + ''', "'''+tk.sender.fullname+'''", "'''+tk.sender.username+'''");' type="button" class="btn btn-primary" data-toggle="tooltip" title="conversation" id="chat_with_user"><i class="fa fa-commenting"></i><input type="hidden" value="''' + str(tk.id) + '''"/></a>
            <button id="''' + str(tk.id) + '''" type="button" class="btn btn-info fw_agent" data-toggle="modal" data-title="forward" data-target="#forward_add"><i class="fa fa-share-square-o" data-toggle="tooltip" title="forward" ></i></button>
            <button id="''' + str(tk.id) + '''" type="button" class="btn btn-info add_agent" data-toggle="modal" data-title="add" data-target="#forward_add"><i class="fa fa-user-plus" data-toggle="tooltip" title="add" ></i></button>'''
            if tem == 1:
                option += r'''<button id="''' + str(tk.id) + '''" disabled type="button" class="btn btn-danger give_up" data-toggle="tooltip" title="give up" ><i class="fa fa-minus-circle"></i></button>'''
            else:
                option += r'''<button id="''' + str(tk.id) + '''" type="button" class="btn btn-danger give_up" data-toggle="tooltip" title="give up" ><i class="fa fa-minus-circle"></i></button>'''
            option +='''<a target="_blank" href="/agent/history/'''+str(tk.id)+ '''" type="button" class="btn btn-warning" data-toggle="tooltip" title="history" ><span class="glyphicon glyphicon-floppy-disk" ></span><i class="fa fa-history"></i></a>'''
            data.append([id, tk.title, topic, handler, status, option])
        ticket = {"data": data}
        tickets = json.loads(json.dumps(ticket))
        return JsonResponse(tickets, safe=False)


def history(request,id):
    if (request.session.has_key('agent')and(Agents.objects.get(username=request.session['agent'])).status == 1) or request.session.has_key('admin'):
        tems = TicketLog.objects.filter(ticketid=id)
        result = []
        for tem in tems:
            if tem.userid is not None:
                action = "<b>User " + str(tem.userid.username) + "</b><br/>"+str(tem.action)
            else:
                action = "<b>Agent " + str(tem.agentid.username) + "</b><br/>"+str(tem.action)
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
        topicag = TopicAgent.objects.filter(agentid=agent)
        list_tp = ""
        for tp1 in topicag:
            list_tp += str(tp1.topicid.name) + "!"
        content = {'forwardin': ForwardTickets.objects.filter(receiverid=agent),
                    'noti_noti': agent.noti_noti,
                    'noti_chat': agent.noti_chat,
                   'addin': AddAgents.objects.filter(receiverid=agent), 
                   'agent_name': mark_safe(json.dumps(agent.username)), 
                   'fullname': mark_safe(json.dumps(agent.fullname)),
                   'list_tp': mark_safe(json.dumps(list_tp))}
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
                        action = "received ticket forward from (agent)" + sender.username
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
        topicag = TopicAgent.objects.filter(agentid=agent)
        list_tp = ""
        for tp1 in topicag:
            list_tp += str(tp1.topicid.name) + "!"
        content ={'forwardout':ForwardTickets.objects.filter(senderid=agent),
                    'noti_noti': agent.noti_noti,
                    'noti_chat': agent.noti_chat,
                    'addout': AddAgents.objects.filter(senderid=agent),
                    'agent_name': mark_safe(json.dumps(agent.username)),
                    'fullname': mark_safe(json.dumps(agent.fullname)),
                    'list_tp': mark_safe(json.dumps(list_tp))}
        if request.method == 'POST':
            if 'forward' in request.POST:
                fwticket = ForwardTickets.objects.get(id=request.POST['tkid'])
                fwticket.delete()
            elif 'add' in request.POST:
                fwticket = AddAgents.objects.get(id=request.POST['tkid'])
                fwticket.delete()
            elif 'noti_noti' in request.POST:
                agent.noti_noti = 0
                agent.save()
            elif 'noti_chat' in request.POST:
                agent.noti_chat = 0
                agent.save()
            
        return render(request,'agent/outbox.html',content)
    else:
        return redirect("/")


def profile(request):
    if request.session.has_key('agent')and(Agents.objects.get(username=request.session['agent'])).status == 1:
        agent = Agents.objects.get(username=request.session['agent'])
        topicag = TopicAgent.objects.filter(agentid=agent)
        list_tp = ""
        for tp1 in topicag:
            list_tp += str(tp1.topicid.name) + "!"
        tpag =[ ta.topicid.name for ta in TopicAgent.objects.filter(agentid=agent)]
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
        return render(request,"agent/profile.html", {'agent': agent, 'noti_noti': agent.noti_noti,
                                                     'noti_chat': agent.noti_chat,
                                                     'topic': tpag,
                                                     'agent_name': mark_safe(json.dumps(agent.username)),
                                                     'fullname': mark_safe(json.dumps(agent.fullname)),
                                                     'list_tp': mark_safe(json.dumps(list_tp))})
    else:
        return redirect("/")


def closed_ticket(request):
    if request.session.has_key('agent')and(Agents.objects.get(username=request.session['agent'])).status == 1:
        agent = Agents.objects.get(username=request.session['agent'])
        tem = Tickets.objects.filter(status=3)
        topicag = TopicAgent.objects.filter(agentid=agent)
        list_tp = ""
        for tp1 in topicag:
            list_tp += str(tp1.topicid.name) + "!"
        content = {'noti_noti': agent.noti_noti,
                    'noti_chat': agent.noti_chat, 
                    'ticket': TicketAgent.objects.filter(agentid=agent, ticketid__in=tem), 
                    'agent_name': mark_safe(json.dumps(agent.username)), 
                    'fullname': mark_safe(json.dumps(agent.fullname)),
                    'list_tp': mark_safe(json.dumps(list_tp))}
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
        topicag = TopicAgent.objects.filter(agentid=agent)
        list_tp = ""
        for tp1 in topicag:
            list_tp += str(tp1.topicid.name) + "!"
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
                    'noti_chat': agent.noti_chat, 
                    'user':users, 
                    'agent_name': mark_safe(json.dumps(agent.username)), 
                    'fullname': mark_safe(json.dumps(agent.fullname)),
                    'list_tp': mark_safe(json.dumps(list_tp))})
    else:
        return redirect("/")


def manage_user_data(request):
    if request.session.has_key('agent')and(Agents.objects.get(username=request.session['agent'])).status == 1:
        users = Users.objects.all()
        data = []
        for us in users:
            if us.status == 0:
                st = r'''<p id="stt''' + str(us.id) +'''"><span class="label label-danger">inactive</span></p>'''
                option = r'''<p id="button''' + str(us.id) +'''"><button id="''' + str(us.id) + '''" class="unblock btn btn-success" type="button" data-toggle="tooltip" title="unblock" ><span class="glyphicon glyphicon glyphicon-ok" ></span> Unblock</button></p>'''
            else:
                st = r'''<p id="stt''' + str(us.id) +'''"><span class="label label-success">active</span></p>'''
                option = r'''<p id="button''' + str(us.id) +'''"><button id="''' + str(us.id) + '''" class="block btn btn-danger" type="button" data-toggle="tooltip" title="block" ><span class="glyphicon glyphicon-lock" ></span> Block</button></p>'''
            data.append([us.id, us.fullname, us.email, us.username, st, str(us.created)[:-13], option])
        ticket = {"data": data}
        tickets = json.loads(json.dumps(ticket))
        return JsonResponse(tickets, safe=False)




