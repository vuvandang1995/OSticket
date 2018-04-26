from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone

from user.models import *
from .forms import ForwardForm, AddForm
from user.forms import CommentForm
from django.core.mail import EmailMessage
import datetime
from django.http import HttpResponse, HttpResponseRedirect
import simplejson as json


# Create your views here.
def home_admin(request):
    if request.session.has_key('admin'):
        admin = Agents.objects.get(username=request.session['admin'])
        list_other = {}
        tk = Tickets.objects.all()
        for tk in tk:
            list_other[tk.id] = list_hd(tk.id)
        content = {'ticket': Tickets.objects.all(), 'handler': TicketAgent.objects.all(), 'admin': admin, 'list_other': list_other.items()}
        if request.method == 'POST':
            if 'close' in request.POST:
                ticketid = request.POST['close']
                tk = Tickets.objects.get(id=ticketid)
                if tk.status == 3:
                    if not TicketAgent.objects.filter(ticketid=tk):
                        tk.status = 0
                    else:
                        tk.status = 1
                else:
                    tk.status = 3
                tk.save()
            elif 'delete' in request.POST:
                ticketid = request.POST['delete']
                tk = Tickets.objects.get(id=ticketid)
                tk.delete()
            elif 'ticketid' in request.POST:
                list_agent = request.POST['list_agent[]']
                list_agent = json.loads(list_agent)
                ticketid = request.POST['ticketid']
                for agentid in list_agent:
                    agent = Agents.objects.get(username=agentid)
                    ticket = Tickets.objects.get(id=ticketid)
                    tkag = TicketAgent(agentid=agent, ticketid=ticket)
                    tkag.save()
                    ticket.status = 1
                    ticket.save()
                    if agent.receive_email == 1:
                        email = EmailMessage(
                            'Forward ticket',
                            render_to_string('agent/mail/forward_mail_leader.html',
                                                {'receiver': agent,
                                                'domain': (get_current_site(request)).domain,
                                                'sender': 'Leader'}),
                            to=[agent.email],
                        )
                        email.send()
        return render(request, 'agent/home_admin.html', content)
    else:
        return redirect('/')


def manager_topic(request):
    if request.session.has_key('admin'):
        admin = Agents.objects.get(username=request.session['admin'])
        content = {'topic': Topics.objects.all(), 'admin': admin}
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
        content = {'agent': Agents.objects.all(), 'admin': admin, 'list_tk': list_tk.items()}
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
                    username =ag.username
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
    if request.session.has_key('agent'):
        content = {'ticket': Tickets.objects.filter(status=0).order_by('dateend'),
                   'agent': Agents.objects.get(username=request.session.get('agent'))}
        return render(request,'agent/home_agent.html',content)
    else:
        return redirect("/")


def assign_ticket(request, id):
    if request.session.has_key('agent'):
        ticket = Tickets.objects.get(id=id)
        agent = Agents.objects.get(username=request.session['agent'])
        ticket.status = 1
        ticket.save()
        TicketAgent.objects.create(agentid=agent, ticketid=ticket)
        user = Users.objects.get(id=ticket.sender.id)
        if user.receive_email == 1:
            email = EmailMessage(
                'Assign ticket',
                render_to_string('agent/mail/assign_mail.html',
                                 {'receiver': user,
                                  'domain': (get_current_site(request)).domain,
                                  'sender': agent,
                                  'ticketid':ticket.id}),
                to=[user.email],
            )
            email.send()
        return redirect("/agent")
    else:
        return redirect("/")


def processing_ticket(request):
    if request.session.has_key('agent'):
        sender = Agents.objects.get(username=request.session['agent'])
        tem = Tickets.objects.filter(status__in=[1, 2]).order_by('status')
        form = ForwardForm()
        form1 = AddForm()
        ticket = TicketAgent.objects.filter(agentid=sender, ticketid__in=tem)
        tic=[]
        for t in ticket:
            tic += [x for x in TicketAgent.objects.filter(ticketid=t.ticketid)]
        content = {'ticket': ticket, 'tic': tic, 'form':form, 'form1': form1}
        if request.method == 'POST':
            if request.POST['type']=='forward':
                form = ForwardForm(request.POST)
                if form.is_valid():
                    ticket = Tickets.objects.get(id=request.POST['ticketid'])
                    receiver = {'receiver': Agents.objects.filter(id__in=form.cleaned_data.get('receiver'))}
                    text = form.cleaned_data.get('content')
                    for rc in receiver['receiver']:
                        if rc != sender:
                            try:
                                TicketAgent.objects.get(ticketid=ticket,agentid=rc)
                            except ObjectDoesNotExist:
                                try:
                                    ForwardTickets.objects.get(senderid=sender, receiverid=rc,ticketid=ticket, content=text)
                                except ObjectDoesNotExist:
                                    ForwardTickets.objects.create(senderid=sender, receiverid=rc, ticketid=ticket,content=text)
                                    if rc.receive_email == 1:
                                        email = EmailMessage(
                                            'Forward ticket',
                                            render_to_string('agent/mail/forward_mail.html',
                                                             {'receiver': rc,
                                                              'domain': (get_current_site(request)).domain,
                                                              'sender': sender}),
                                            to=[rc.email],
                                        )
                                        email.send()
                return redirect("/agent/processing_ticket")
            else:
                form1 = AddForm(request.POST)
                if form1.is_valid():
                    ticket = Tickets.objects.get(id=request.POST['ticketid'])
                    receiver = {'receiver': Agents.objects.filter(id__in=form1.cleaned_data.get('receiver'))}
                    text = form1.cleaned_data.get('content')
                    for rc in receiver['receiver']:
                        if rc != sender:
                            try:
                                TicketAgent.objects.get(ticketid=ticket,agentid=rc)
                            except ObjectDoesNotExist:
                                try:
                                    AddAgents.objects.get(senderid=sender, receiverid=rc, ticketid=ticket,content=text)
                                except ObjectDoesNotExist:
                                    AddAgents.objects.create(senderid=sender, receiverid=rc, ticketid=ticket, content=text)
                                    if rc.receive_email == 1:
                                        email = EmailMessage(
                                            'Add in a ticket',
                                            render_to_string('agent/mail/add_mail.html',
                                                             {'receiver': rc,
                                                              'domain': (get_current_site(request)).domain,
                                                              'sender': sender}),
                                            to=[rc.email]
                                        )
                                        email.send()
                return redirect("/agent/processing_ticket")
        return render(request,'agent/processing_ticket.html',content)
    else:
        return redirect("/")


def process(request, id):
    if request.session.has_key('agent'):
        ticket = Tickets.objects.get(id=id)
        ticket.status = 1
        ticket.save()
        return redirect("/agent/processing_ticket")
    else:
        return redirect("/")


def done(request,id):
    if request.session.has_key('agent'):
        agent = Agents.objects.get(username=request.session['agent'])
        ticket = Tickets.objects.get(id=id)
        ticket.status = 2
        ticket.save()
        user = Users.objects.get(id=ticket.sender.id)
        if user.receive_email == 1:
            email = EmailMessage(
                'Finished ticket',
                render_to_string('agent/mail/done_mail.html',
                                 {'receiver': user,
                                  'domain': (get_current_site(request)).domain,
                                  'sender': agent,
                                  'ticketid':ticket.id}),
                to=[user.email],
            )
            email.send()
        return redirect("/agent/processing_ticket")
    else:
        return redirect("/")


def give_up(request,id):
    if request.session.has_key('agent'):
        agent = Agents.objects.get(username=request.session['agent'])
        ticket = Tickets.objects.get(id=id)
        try:
            TicketAgent.objects.get(ticketid=ticket)
        except MultipleObjectsReturned:
            tk = TicketAgent.objects.get(ticketid=ticket,agentid=agent)
            tk.delete()
        return redirect("/agent/processing_ticket")
    else:
        return redirect("/")


def inbox(request):
    if request.session.has_key('agent'):
        agent = Agents.objects.get(username=request.session.get('agent'))
        content ={'forwardin': ForwardTickets.objects.filter(receiverid=agent),
                  'addin': AddAgents.objects.filter(receiverid=agent)}
        return render(request,'agent/inbox.html',content)
    else:
        return redirect("/")


def outbox(request):
    if request.session.has_key('agent'):
        agent = Agents.objects.get(username=request.session.get('agent'))
        content ={'forwardout':ForwardTickets.objects.filter(senderid=agent),
                  'addout': AddAgents.objects.filter(senderid=agent)}
        return render(request,'agent/outbox.html',content)
    else:
        return redirect("/")


def profile(request):
    if request.session.has_key('agent'):
        agent = Agents.objects.get(username=request.session['agent'])
        if request.method == 'POST':
            if 'fullname' in request.POST:
                agent.fullname = request.POST['fullname']
                agent.email = request.POST['email']
                agent.phone = request.POST['phone']
                agent.receive_email = request.POST['receive']
                agent.save()
            elif 'pwd' in request.POST:
                agent.password = request.POST['pwd']
                agent.save()
        return render(request,"agent/profile.html",{'agent':agent})
    else:
        return redirect("/")


def accept_forward(request,id):
    if request.session.has_key('agent'):
        agent = Agents.objects.get(username=request.session.get('agent'))
        ticket = Tickets.objects.get(id=id)
        fwticket = ForwardTickets.objects.get(ticketid=ticket,receiverid=agent)
        sender = fwticket.senderid
        agticket = TicketAgent.objects.get(ticketid=ticket,agentid=fwticket.senderid)
        fwticket.delete()
        try:
            TicketAgent.objects.get(ticketid=ticket, agentid=agent)
        except TicketAgent.DoesNotExist:
            agticket.agentid = agent
            agticket.save()
            if sender.receive_email == 1:
                email = EmailMessage(
                    'Accept forward request',
                    render_to_string('agent/mail/accept_mail.html',
                                     {'receiver': sender,
                                      'domain': (get_current_site(request)).domain,
                                      'sender': agent}),
                    to=[sender.email]
                )
                email.send()
        else:
            agticket.delete()
        # return render(request,'agent/inbox.html',{'forwardin':ForwardTickets.objects.filter(receiverid=agent),
        #           'addin': AddAgents.objects.filter(receiverid=agent)})
        return redirect("/agent/inbox")
    else:
        return redirect("/")


def deny_forward(request,id):
    if request.session.has_key('agent'):
        agent = Agents.objects.get(username=request.session.get('agent'))
        ticket = Tickets.objects.get(id=id)
        fwticket = ForwardTickets.objects.get(ticketid=ticket,receiverid=agent)
        sender = fwticket.senderid
        fwticket.delete()
        if sender.receive_email == 1:
            email = EmailMessage(
                'Deny forward request',
                render_to_string('agent/mail/deny_mail.html',
                                 {'receiver': sender,
                                  'domain': (get_current_site(request)).domain,
                                  'sender': agent}),
                to=[sender.email]
            )
            email.send()
        # return render(request,'agent/inbox.html',{'forwardin':ForwardTickets.objects.filter(receiverid=agent),
        #           'addin': AddAgents.objects.filter(receiverid=agent)})
        return redirect("/agent/inbox")
    else:
        return redirect("/")


def cancel_forward(request,id):
    if request.session.has_key('agent'):
        fwticket = ForwardTickets.objects.get(id=id)
        fwticket.delete()
        agent = Agents.objects.get(username=request.session.get('agent'))
        content = {'forwardout': ForwardTickets.objects.filter(senderid=agent),
                   'addout': AddAgents.objects.filter(senderid=agent)}
        return render(request, 'agent/outbox.html', content)
    else:
        return redirect("/")


def accept_add(request,id):
    if request.session.has_key('agent'):
        agent = Agents.objects.get(username=request.session.get('agent'))
        ticket = Tickets.objects.get(id=id)
        fwticket = AddAgents.objects.get(ticketid=ticket,receiverid=agent)
        sender = fwticket.senderid
        try:
            TicketAgent.objects.get(ticketid=ticket, agentid=agent)
        except TicketAgent.DoesNotExist:
            TicketAgent.objects.create(ticketid=ticket, agentid=agent)
            if sender.receive_email == 1:
                email = EmailMessage(
                    'Accept add request',
                    render_to_string('agent/mail/accept_mail.html',
                                     {'receiver': sender,
                                      'domain': (get_current_site(request)).domain,
                                      'sender': agent}),
                    to=[sender.email]
                )
                email.send()
        fwticket.delete()
        # return render(request,'agent/inbox.html',{'forwardin':ForwardTickets.objects.filter(receiverid=agent),
        #         #           'addin': AddAgents.objects.filter(receiverid=agent)})
        return redirect("/agent/inbox")
    else:
        return redirect("/")


def deny_add(request,id):
    if request.session.has_key('agent'):
        agent = Agents.objects.get(username=request.session.get('agent'))
        ticket = Tickets.objects.get(id=id)
        fwticket = AddAgents.objects.get(ticketid=ticket,receiverid=agent)
        sender = fwticket.senderid
        if sender.receive_email == 1:
            email = EmailMessage(
                'Deny add request',
                render_to_string('agent/mail/deny_mail.html',
                                 {'receiver': sender,
                                  'domain': (get_current_site(request)).domain,
                                  'sender': agent}),
                to=[sender.email]
            )
            email.send()
        fwticket.delete()
        # return render(request,'agent/inbox.html',{'forwardin':ForwardTickets.objects.filter(receiverid=agent),
        #           'addin': AddAgents.objects.filter(receiverid=agent)})
        return redirect("/agent/inbox")
    else:
        return redirect("/")


def cancel_add(request,id):
    if request.session.has_key('agent'):
        fwticket = AddAgents.objects.get(id=id)
        fwticket.delete()
        agent = Agents.objects.get(username=request.session.get('agent'))
        content = {'forwardout': ForwardTickets.objects.filter(senderid=agent),
                   'addout': AddAgents.objects.filter(senderid=agent)}
        return render(request, 'agent/outbox.html', content)
    else:
        return redirect("/")


def closed_ticket(request):
    if request.session.has_key('agent'):
        agent = Agents.objects.get(username=request.session['agent'])
        tem = Tickets.objects.filter(status=3)
        content = {'ticket': TicketAgent.objects.filter(agentid=agent, ticketid__in=tem)}
        return render(request,'agent/closed_ticket.html', content)
    else:
        return redirect("/")


def manager_user(request):
    if request.session.has_key('agent'):
        users = Users.objects.all()
        return render(request,"agent/manage_user.html",{'user':users})
    else:
        return redirect("/")


def block_user(request,id):
    if request.session.has_key('agent'):
        users = Users.objects.all()
        user = Users.objects.get(id=id)
        user.status = 0
        user.save()
        return render(request,"agent/manage_user.html",{'user':users})
    else:
        return redirect("/")


def unblock_user(request,id):
    if request.session.has_key('agent'):
        users = Users.objects.all()
        user = Users.objects.get(id=id)
        user.status = 1
        user.save()
        return render(request,"agent/manage_user.html",{'user':users})
    else:
        return redirect("/")


def conversation(request,id):
    if request.session.has_key('agent'):
        agent = Agents.objects.get(username=request.session['agent'])
        ticket = get_object_or_404(Tickets, pk=id)
        comments = Comments.objects.filter(ticketid=ticket).order_by('date')
        content = {'agent': agent, 'ticket': ticket, 'comments': comments}
        if request.method == 'POST':
            Comments.objects.create(ticketid=ticket,
                                    agentid=agent,
                                    content=request.POST['content'],
                                    date=timezone.now())
        return render(request, 'agent/conversation.html', content)
    else:
        return redirect("/")