from django.shortcuts import render, redirect
from user.models import *
from .forms import AddOrForwardForm
from django.http import HttpResponse, HttpResponseRedirect
import simplejson as json

# Create your views here.
def home_admin(request):
    if request.session.has_key('admin'):
        admin = Agents.objects.get(username=request.session['admin'])
        content = {'ticket': Tickets.objects.all(), 'handler': TicketAgent.objects.all(), 'admin': admin, 'agent': Agents.objects.all()}
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
            elif 'ticketid' in request.POST:
                list_agent = request.POST['list_agent[]']
                list_agent = json.loads(list_agent)
                ticketid = request.POST['ticketid']
                for agentid in list_agent:
                    agent = Agents.objects.get(id=agentid)
                    ticket = Tickets.objects.get(id=ticketid)
                    tkag = TicketAgent(agentid=agent, ticketid=ticket)
                    tkag.save()
                    ticket.status = 1
                    ticket.save()
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
        content = {'agent': Agents.objects.all(), 'admin': admin, 'tkag': TicketAgent.objects.all()}
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
                    username = request.POST['username']
                    password = request.POST['password']
                    ag = Agents(fullname=fullname, username=username, email=email, password=password)
                    ag.save()
                else:
                    ag = Agents.objects.get(id=request.POST['agentid'])
                    fullname = request.POST['add_agent']
                    email = request.POST['email']
                    username = request.POST['username']
                    ag.fullname = fullname
                    ag.email = email
                    ag.username = username
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
        form = AddOrForwardForm()
        content ={'ticket': TicketAgent.objects.filter(agentid=sender, ticketid__in=tem),'form': form}
        if request.method == 'POST':
            form = AddOrForwardForm(request.POST)
            if form.is_valid():
                ticket = Tickets.objects.get(id=request.POST['ticketid'])
                receiver = {'receiver': Agents.objects.filter(id__in=form.cleaned_data.get('receiver'))}
                for rc in receiver['receiver']:
                    if rc != sender:
                        ForwardTickets.objects.get_or_create(senderid=sender,receiverid=rc,ticketid=ticket)
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


def forward_ticket(request):
    if request.session.has_key('agent'):
        agent = Agents.objects.get(username=request.session.get('agent'))
        content ={'ticket':ForwardTickets.objects.filter(receiverid=agent)}
        return render(request,'agent/forward_ticket.html',content)
    else:
        return redirect("/")


def accept_forward(request,id):
    if request.session.has_key('agent'):
        agent = Agents.objects.get(username=request.session.get('agent'))
        ticket = Tickets.objects.get(id=id)
        fwticket = ForwardTickets.objects.get(ticketid=ticket,receiverid=agent)
        fwticket.delete()
        agticket = TicketAgent.objects.get(ticketid=ticket)
        agticket.agentid = agent
        agticket.save()
        return render(request,'agent/forward_ticket.html',{'ticket':ForwardTickets.objects.filter(receiverid=agent)})
    else:
        return redirect("/")

def deny_forward(request,id):
    if request.session.has_key('agent'):
        agent = Agents.objects.get(username=request.session.get('agent'))
        ticket = Tickets.objects.get(id=id)
        fwticket = ForwardTickets.objects.get(ticketid=ticket,receiverid=agent)
        fwticket.delete()
        return render(request,'agent/forward_ticket.html',{'ticket':ForwardTickets.objects.filter(receiverid=agent)})
    else:
        return redirect("/")


def accept_add(request,id):
    if request.session.has_key('agent'):
        agent = Agents.objects.get(username=request.session.get('agent'))
        ticket = Tickets.objects.get(id=id)
        fwticket = ForwardTickets.objects.get(ticketid=ticket,receiverid=agent)
        fwticket.delete()
        TicketAgent.objects.create(ticketid=ticket,agentid=agent)
        return render(request,'agent/forward_ticket.html',{'ticket':ForwardTickets.objects.filter(receiverid=agent)})
    else:
        return redirect("/")


def deny_add(request,id):
    if request.session.has_key('agent'):
        agent = Agents.objects.get(username=request.session.get('agent'))
        ticket = Tickets.objects.get(id=id)
        fwticket = ForwardTickets.objects.get(ticketid=ticket,receiverid=agent)
        fwticket.delete()
        return render(request,'agent/forward_ticket.html',{'ticket':ForwardTickets.objects.filter(receiverid=agent)})
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