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
from django.contrib.auth import (
    get_user_model,
    login,
    logout
)
from .forms import *
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test

MAX_UPLOAD_SIZE = 10485760


def homeuser(request):
    if request.session.has_key('username'):
        user = Users.objects.get(username=request.session['username'])
        form = CreateNewTicketForm()
        content = {'ticket': Tickets.objects.filter(sender=user.id),'form':form}
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


def detail(request):
    if request.session.has_key('username'):
        user = Users.objects.get(username=request.session['username'])
        return render(request, 'user/detail.html', {'user': user})
    else:
        return redirect("/")


def login_user(request):
    form = UserLoginForm()
    if request.method == 'POST':
        if 'fullname' and 'email' and 'password2' not in request.POST:
            form = UserLoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate_user(request, username=username, password=password)
                if user is not None:
                    request.session['username'] = username
                    return redirect("/user")
                else:
                    return redirect("/")
        else:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                current_site = get_current_site(request)
                user = form.save()
                mail_subject = 'Activate your blog account.'
                message = render_to_string('acc_active_email.html', {
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
                return HttpResponse('Please confirm your email address to complete the registration')
            else:
                return redirect('/')
    return render(request, 'user/index.html',{})


def logout_user(request):
    del request.session['username']
    return redirect("/")


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Users.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.status = 1
        user.save()
        #request.session['username'] = username
        return redirect("/")
        mess = 'Thank you for your email confirmation. Now you can login your account.'
        # return render(request, 'user/index.html',{'mess': mess})
        
    else:
        return HttpResponse('Activation link is invalid!')


# def create_ticket(request):
#     if request.session.has_key('username'):
#         user = Users.objects.get(username=request.session['username'])
#         form = CreateNewTicketForm()
#         if request.method == 'POST':
#             form = CreateNewTicketForm(request.POST,request.FILES)
#             if form.is_valid():
#                 topic = Topics.objects.get(id=form.cleaned_data['topic'])
#                 if request.FILES.get('attach') is None:
#                     Tickets.objects.create(title="abc", content='abc', sender=user,
#                                            topicid=topic, datestart=timezone.now(),
#                                            dateend=(timezone.now() + timezone.timedelta(days=3)))
#                     return redirect("/")
#                 else:
#                     if request.FILES['attach']._size > MAX_UPLOAD_SIZE:
#                         return render(request, 'user/create_ticket.html', {'form': form})
#                     else:
#                         Tickets.objects.create(title="abc", content='abc', sender=user,
#                                                        topicid=topic, datestart=timezone.now(),
#                                                        dateend=(timezone.now()+timezone.timedelta(days=3)),
#                                                        attach=request.FILES['attach'])
#                         handle_uploaded_file(request.FILES['attach'])
#                         return redirect("/")
#             else:
#                 print("form invalid")
#                 return render(request, 'user/create_ticket.html', {'form': form})
#         else:
#             return render(request, 'user/create_ticket.html', {'form': form})
#     else:
#         return redirect("/")



