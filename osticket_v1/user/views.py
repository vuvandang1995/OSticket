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
from django.http import Http404
from django.views import generic
from django.urls import reverse
from .forms import *
import string
import datetime
from random import *
min_char = 8
max_char = 12
allchar = string.ascii_letters + string.digits

MAX_UPLOAD_SIZE = 10485760
dic = {}
dic_time = {}


def homeuser(request):
    if request.session.has_key('user'):
        user = Users.objects.get(username=request.session['user'])
        form = CreateNewTicketForm()
        ticket = Tickets.objects.filter(sender=user.id).order_by('status')
        atic = TicketAgent.objects.filter(ticketid__in=ticket)
        content = {'ticket': ticket,
                   'form': form,
                   'user': user,
                   'atic': atic}
        if request.method == 'POST':
            form = CreateNewTicketForm(request.POST,request.FILES)
            if form.is_valid():
                topic = Topics.objects.get(id=form.cleaned_data['topic'])
                if request.FILES.get('attach') is None:
                    Tickets.objects.create(title=form.cleaned_data['title'], content=form.cleaned_data['content'],
                                           sender=user,topicid=topic, datestart=timezone.now(),
                                           dateend=(timezone.now() + timezone.timedelta(days=3)))
                else:
                    if request.FILES['attach']._size < MAX_UPLOAD_SIZE:
                        Tickets.objects.create(title=form.cleaned_data['title'],content=form.cleaned_data['content'],
                                               sender=user,topicid=topic, datestart=timezone.now(),
                                               dateend=(timezone.now()+timezone.timedelta(days=3)),
                                               attach=request.FILES['attach'])
                        handle_uploaded_file(request.FILES['attach'])
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
        ticket = Tickets.objects.get(id=id)
        ticket.status = 3
        ticket.save()
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
                u.fullname = fullname
                u.email = email
                u.phone = phone
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
                        return redirect('/agent')
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


def create_ticket(request):
    if request.session.has_key('user'):
        user = Users.objects.get(username=request.session['user'])
        form = CreateNewTicketForm()
        if request.method == 'POST':
            form = CreateNewTicketForm(request.POST,request.FILES)
            if form.is_valid():
                topic = Topics.objects.get(id=form.cleaned_data['topic'])
                Tickets.objects.create(title="abc", content='abc', sender=user,
                                       topicid=topic, datestart=timezone.now(),
                                       dateend=(timezone.now()+timezone.timedelta(days=3)),
                                       attach=request.FILES['attach'])
                handle_uploaded_file(request.FILES['attach'])
                return redirect("/")
            else:
                print("form invalid")
                return render(request, 'user/create_ticket.html', {'form': form})
        else:
            return render(request, 'user/create_ticket.html', {'form': form})
    else:
        return redirect("/")


def conversation(request,id):
    if request.session.has_key('user'):
        user = Users.objects.get(username=request.session['user'])
        ticket = get_object_or_404(Tickets, pk=id)
        form = CommentForm()
        comments = Comments.objects.filter(ticketid=ticket).order_by('date')
        content = {'user': user, 'ticket': ticket, 'form': form, 'comments': comments}
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                Comments.objects.create(ticketid=ticket,
                                        userid=user,
                                        content=form.cleaned_data['content'],
                                        date=timezone.now())
                redirect("{% url 'user:conversation' ticket.id %}")
        return render(request, 'user/conversation.html',content)
    else:
        return redirect("/")