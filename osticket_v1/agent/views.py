from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.shortcuts import render, redirect
from user.models import *
from .forms import ForwardForm, AddForm
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.


def home_admin(request):
    if request.session.has_key('admin'):
        admin = Agents.objects.get(username=request.session['admin'])
        content = {'ticket': Tickets.objects.all(), 'handler': TicketAgent.objects.all(), 'admin': admin}
        if request.method == 'POST':
            if 'close' in request.POST:
                ticketid = request.POST['close']
                tk = Tickets.objects.get(id=ticketid)
                if tk.status == 3:
                    tk.status = 0
                else:
                    tk.status = 3
                tk.save()
            elif 'delete' in request.POST:
                ticketid = request.POST['delete']
                tk = Tickets.objects.get(id=ticketid)
                tk.delete()
            elif 'forward' in request.POST:
                print('forward')
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
                    tp = Topics(name=topicname)
                    tp.save()
                else:
                    tp = Topics.objects.get(id=request.POST['topicid'])
                    tp.name = request.POST['add_topic']
                    tp.save()
        return render(request, 'agent/manager_topic.html', content)
    else:
        return redirect('/')


def manager_agent(request):
    if request.session.has_key('admin'):
        admin = Agents.objects.get(username=request.session['admin'])
        content = {'agent': Agents.objects.all(), 'admin': admin}
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
        content ={'ticket': ticket,'tic': tic,'form': form, 'form1':form1}
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
                                ForwardTickets.objects.get_or_create(senderid=sender,receiverid=rc,ticketid=ticket,content=text)

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
                                AddAgents.objects.get_or_create(senderid=sender, receiverid=rc, ticketid=ticket,content=text)
        return render(request,'agent/processing_ticket.html', content)
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
        ticket = Tickets.objects.get(id=id)
        ticket.status = 2
        ticket.save()
        return redirect("/agent/processing_ticket")
    else:
        return redirect("/")


def give_up(request,id):
    if request.session.has_key('agent'):
        agent = Agents.objects.get(username=request.session['agent'])
        ticket = Tickets.objects.get(id=id)
        try :
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


def accept_forward(request,id):
    if request.session.has_key('agent'):
        agent = Agents.objects.get(username=request.session.get('agent'))
        ticket = Tickets.objects.get(id=id)
        fwticket = ForwardTickets.objects.get(ticketid=ticket,receiverid=agent)
        agticket = TicketAgent.objects.get(ticketid=ticket,agentid=fwticket.senderid)
        fwticket.delete()
        try:
            TicketAgent.objects.get(ticketid=ticket, agentid=agent)
        except TicketAgent.DoesNotExist:
            agticket.agentid = agent
            agticket.save()
        else:
            agticket.delete()
        return render(request,'agent/inbox.html',{'forwardin':ForwardTickets.objects.filter(receiverid=agent),
                  'addin': AddAgents.objects.filter(receiverid=agent)})
    else:
        return redirect("/")


def deny_forward(request,id):
    if request.session.has_key('agent'):
        agent = Agents.objects.get(username=request.session.get('agent'))
        ticket = Tickets.objects.get(id=id)
        fwticket = ForwardTickets.objects.get(ticketid=ticket,receiverid=agent)
        fwticket.delete()
        return render(request,'agent/inbox.html',{'forwardin':ForwardTickets.objects.filter(receiverid=agent),
                  'addin': AddAgents.objects.filter(receiverid=agent)})
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
        try:
            TicketAgent.objects.get(ticketid=ticket, agentid=agent)
        except TicketAgent.DoesNotExist:
            TicketAgent.objects.create(ticketid=ticket, agentid=agent)
        fwticket.delete()


        return render(request,'agent/inbox.html',{'forwardin':ForwardTickets.objects.filter(receiverid=agent),
                  'addin': AddAgents.objects.filter(receiverid=agent)})
    else:
        return redirect("/")


def deny_add(request,id):
    if request.session.has_key('agent'):
        agent = Agents.objects.get(username=request.session.get('agent'))
        ticket = Tickets.objects.get(id=id)
        fwticket = AddAgents.objects.get(ticketid=ticket,receiverid=agent)
        fwticket.delete()
        return render(request,'agent/inbox.html',{'forwardin':ForwardTickets.objects.filter(receiverid=agent),
                  'addin': AddAgents.objects.filter(receiverid=agent)})
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


def assign_ticket(request,id):
    if request.session.has_key('agent'):
        ticket = Tickets.objects.get(id=id)
        agent = Agents.objects.get(username=request.session['agent'])
        ticket.status = 1
        ticket.save()
        TicketAgent.objects.create(agentid=agent, ticketid=ticket)
        return redirect("/agent")
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