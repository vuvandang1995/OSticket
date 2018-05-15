from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.shortcuts import get_object_or_404, render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.utils.safestring import mark_safe
import json

from django.http import Http404
from django.views import generic
from django.urls import reverse
from .forms import *
import string
import datetime
from random import *
from django.template.defaulttags import register
min_char = 8
max_char = 12
allchar = string.ascii_letters + string.digits

MAX_UPLOAD_SIZE = 10485760
dic = {}
dic_time = {}


def history(request,id):
    if request.session.has_key('user'):
        tems = TicketLog.objects.filter(ticketid=id)
        result = []
        for tem in tems:
            if tem.userid is not None:
                action = "<b>" + str(tem.action) + "</b>" + "<br/> by user "+str(tem.userid.fullname)
            else:
                action = "<b>" + str(tem.action) + "</b>" + "<br/> by agent "+str(tem.agentid.fullname)
            result.append({"id": tem.id,
                           "content": action,
                           "group": "period",
                           "start": str(tem.date)+"T"+str(tem.time)[:-7]})
        maxtime = TicketLog.objects.filter(ticketid=id).latest('id')
        mintime = TicketLog.objects.filter(ticketid=id).earliest('id')
        if maxtime != mintime:
            if maxtime.ticketid.status == 1:
                status = 'processing'
            elif maxtime.ticketid.status == 2:
                status = 'done'
            else:
                status = 'close'
            tim = str(timezone.datetime.combine(maxtime.date, maxtime.time) - timezone.datetime.combine(
                mintime.date, mintime.time))[:-7]
            result.append({"id": 0,
                           "content": "Ticket no."+str(id)+" (status: " + status + ") (exist time " + tim + ")",
                           "className": "expected",
                           "group": "overview",
                           "start": str(mintime.date) + "T" + str(mintime.time)[:-7],
                           "end": str(maxtime.date) + "T" + str(maxtime.time)[:-7]})
        tk = json.loads(json.dumps(result))
        return render(request, 'user/history.html', {'tk': tk, 'id': str(id)})
    else:
        return redirect("/")


def homeuser(request):
    if request.session.has_key('user'):
        user = Users.objects.get(username=request.session['user'])
        admin = Agents.objects.get(admin=1)
        form = CreateNewTicketForm()
        topic = Topics.objects.all()
        ticket = Tickets.objects.filter(sender=user.id).order_by('datestart').reverse()
        handler = TicketAgent.objects.all()
        receiver = Agents.objects.all()
        content = {'ticket': ticket,
                   'form': form,
                   'user': user,
                   'handler': handler,
                   'topic': topic,
                   'username': mark_safe(json.dumps(user.username))
                   }
        if request.method == 'POST':
            form = CreateNewTicketForm(request.POST,request.FILES)
            if form.is_valid():
                topicA = Topics.objects.get(id=request.POST['topic'])
                ticket = Tickets()
                ticket.title = form.cleaned_data['title']
                ticket.content = form.cleaned_data['content']
                ticket.sender = user
                ticket.topicid = topicA
                ticket.datestart = timezone.now()
                ticket.dateend = (timezone.now() + timezone.timedelta(days=3))
                if request.FILES.get('attach') is not None:
                    if request.FILES['attach']._size < MAX_UPLOAD_SIZE:
                        ticket.attach = request.FILES['attach']
                        handle_uploaded_file(request.FILES['attach'])
                    else:
                        return render(request, 'user/home_user.html', content)
                ticket.save()
                TicketLog.objects.create(userid=user,
                                         ticketid=ticket,
                                         action='create ticket',
                                         date=timezone.now().date(),
                                         weekday=get_weekday(),
                                         time=timezone.now().time())
                if topicA.type_send == 1:
                    for rc in receiver:
                        if rc.receive_email == 1:
                            email = EmailMessage('New ticket',
                                                render_to_string('user/new_ticket.html', {}),
                                                to=[rc.email],)
                            email.send()
                else:
                    email = EmailMessage('New ticket',
                                        render_to_string('user/new_ticket.html', {}),
                                        to=[admin.email],)
                    email.send()
            return redirect("/user")
        else:
            return render(request, 'user/home_user.html', content)
    else:
        return redirect("/")


def handle_uploaded_file(f):
    path = "media/photos/"+f.name
    file = open(path, 'wb+')
    for chunk in f.chunks():
        file.write(chunk)
    file.close()


def close_ticket(request,id):
    if request.session.has_key('user'):
        sender = Users.objects.get(username=request.session['user'])
        ticket = Tickets.objects.get(id=id)
        ticket.status = 3
        ticket.save()
        TicketLog.objects.create(userid=sender,
                                 ticketid=ticket,
                                 action='close ticket',
                                 date=timezone.now().date(),
                                 weekday=get_weekday(),
                                 time=timezone.now().time())
        try:
            tkag = TicketAgent.objects.filter(ticketid=id).values('agentid')
        except ObjectDoesNotExist:
            pass
        else:
            receiver = Agents.objects.filter(id__in=tkag)
            for rc in receiver:
                if rc.receive_email == 1:
                    email = EmailMessage('Closed ticket',
                                         render_to_string('user/close_email.html',{'receiver': rc,'sender': sender,'id':id}),
                                         to=[rc.email],)
                    email.send()
        return redirect("/user")
    else:
        return redirect("/")


def detail_user(request):
    if request.session.has_key('user'):
        user = Users.objects.get(username=request.session['user'])
        if request.method == 'POST':
            if 'change_user' in request.POST:
                u = Users.objects.get(id=request.POST['userid'])
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
                u = Users.objects.get(id=request.POST['userid'])
                u.password = request.POST['pwd']
                u.save()
        return render(request, 'user/detail_user.html', {'user': user})
    else:
        return redirect("/")


def login_user(request):
    mess_resetpwd_error = 'Email chưa được đăng kí hoặc không đúng định dạng'
    mess_resetpwd_ok = 'Please confirm your email address to reset your account'
    mess_register_error = 'Thông tin đăng kí không hợp lệ'
    mess_register_ok = 'Please confirm your email address to complete the registration'
    mess_admin_ok = 'Please confirm your email address to complete the login admin'
    mess_login_error = 'Thông tin đăng nhập không hợp lệ'
    if request.session.has_key('user'):
        return redirect("/user")
    elif request.session.has_key('agent'):
        return redirect('/agent')
    elif request.session.has_key('admin'):
        return redirect('/agent/admin')
    else:
        if request.method == 'POST':
            # post form để User yêu cầu reset mật khẩu, gửi link về mail
            if 'uemail' in request.POST:
                print(request.POST)
                form = UserResetForm(request.POST)
                if form.is_valid():
                    to_email = form.cleaned_data['uemail']
                    current_site = get_current_site(request)
                    user = get_user_email(to_email)
                    mail_subject = 'Reset password your account.'
                    message = render_to_string('user/resetpwd.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(user.id)).decode(),
                        'token':account_activation_token.make_token(user),
                    })
                    email = EmailMessage(
                                mail_subject, message, to=[to_email]
                    )
                    email.send()
                    return render(request, 'user/index.html',{'mess': mess_resetpwd_ok})
                else:
                    return render(request, 'user/index.html',{'mess': mess_resetpwd_error})
            # Post form User đăng kí tài khoản, gửi link xác nhận về mail
            elif 'fullname' and 'email' and 'password2' in request.POST:
                form = RegistrationForm(request.POST)
                if form.is_valid():
                    current_site = get_current_site(request)
                    user = form.save()
                    mail_subject = 'Activate your blog account.'
                    message = render_to_string('user/acc_active_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(user.id)).decode(),
                        'token':account_activation_token.make_token(user),
                    })
                    to_email = form.cleaned_data['email']
                    email = EmailMessage(
                                mail_subject, message, to=[to_email]
                    )
                    email.send()
                    return render(request, 'user/index.html',{'mess': mess_register_ok})
                else:
                    return render(request, 'user/index.html',{'mess': mess_register_error})
            # Agent đăng nhập, nếu là agent thường thì login bình thường, Maser-admin thì cần code xác thực
            elif 'agentname' and 'agentpass' in request.POST:
                form = AgentLoginForm(request.POST)
                if form.is_valid():
                    agentname = form.cleaned_data['agentname']
                    agentpass = form.cleaned_data['agentpass']
                    if authenticate_agent(agentname=agentname, agentpass=agentpass) is None:
                        return render(request, 'user/index.html',{'mess': mess_login_error})
                    elif authenticate_agent(agentname=agentname, agentpass=agentpass) == 1:
                        agent = get_agent(agentname)
                        mail_subject = 'Mã xác thực đăng nhập.'
                        code = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
                        dic[agent.username] = code
                        now = datetime.datetime.now()
                        expiry_date = now + datetime.timedelta(minutes = 1)
                        dic_time[code] = expiry_date
                        message = render_to_string('user/confirm_admin.html', {
                        'agent': agent,
                        'code': code,
                        })
                        to_email = agent.email
                        email = EmailMessage(
                                    mail_subject, message, to=[to_email]
                        )
                        email.send()
                        return redirect('/submitadmin')
                    elif authenticate_agent(agentname=agentname, agentpass=agentpass) == 0:
                        request.session['agent'] = agentname
                        return redirect('/agent/')
                else:
                    return render(request, 'user/index.html',{'mess': mess_login_error})
            # User đăng nhập
            else:
                form = UserLoginForm(request.POST)
                if form.is_valid():
                    username = form.cleaned_data['username']
                    request.session['user'] = username
                    return redirect("/user")
                else:
                    return render(request, 'user/index.html',{'mess': mess_login_error})
        return render(request, 'user/index.html', {})


def logout_user(request):
    del request.session['user']
    return redirect("/")


def activate(request, uidb64, token):
    mess_active_error = 'Activation link is invalid!'
    mess_active_ok = ''
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Users.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.status = 1
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        mess = 'Thank you for your email confirmation. Now you can login your account.'
        # return render(request, 'user/index.html',{'mess': mess})
        # return redirect('/', {'mess': mess})
    else:
        return HttpResponse('Activation link is invalid!')


def resetpwd(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Users.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = ResetForm(request.POST)
            if form.is_valid():
                user.password = form.cleaned_data
                user.save()
                return redirect('/')
            else:
                return redirect('/')
        return render(request, 'user/formresetpass.html', {})
    else:
        return HttpResponse('Activation link is invalid!')


def submitadmin(request):
    mess = 'Please confirm your email address to complete the login admin'
    mess_code_error = 'Code sai rồi bạn ơi'
    mess_time_error = 'Code hết hạn rồi bạn ơi'
    if request.method == 'POST':
        if request.POST['code'] in dic.values():
            if datetime.datetime.now() < dic_time[request.POST['code']]:
                for agentname, code in dic.items():
                    if code == request.POST['code']:
                        request.session['admin'] = agentname
                        return redirect('/agent/admin')
            else:
                return render(request, 'user/submit_code_admin.html', {'mess': mess_time_error})
        else:
            return render(request, 'user/submit_code_admin.html', {'mess': mess_code_error})
    return render(request, 'user/submit_code_admin.html', {'mess': mess})


def conversation(request,id):
    if request.session.has_key('user'):
        user = Users.objects.get(username=request.session['user'])
        ticket = get_object_or_404(Tickets, pk=id)
        try:
            hd = TicketAgent.objects.filter(ticketid=ticket)
        except:
            hd = None
        if hd is not None and ticket.sender == user:
            if ticket.chat is None:
                room_name = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
                ticket.chat = room_name
                ticket.save()
            tk = mark_safe(json.dumps(ticket.chat))
        else:
            return redirect('/user')
        
        # form = CommentForm()
        comments = Comments.objects.filter(ticketid=ticket).order_by('date')
        content = {'user': user, 'ticket': ticket, 'comments': comments, 'room_name_json': tk, 'who': 'me'}
        if request.method == 'POST':
            # form = CommentForm(request.POST)//
            # if form.is_valid():
            Comments.objects.create(ticketid=ticket,
                                    userid=user,
                                    content=request.POST['content'],
                                    date=timezone.now())
        return render(request, 'user/conversation.html',content)
    else:
        return redirect("/")