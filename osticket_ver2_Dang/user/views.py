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


def homeuser(request):
    if request.session.has_key('username'):
        print(request.session.session_key)
        user = Users.objects.get(username=request.session['username'])
        return render(request, 'user/home_user.html', {'user': user})
    else:
        return redirect("/")

def detail(request):
    if request.session.has_key('username'):
        user = Users.objects.get(username=request.session['username'])
        return render(request, 'user/detail.html', {'user': user})
    else:
        return redirect("/")

def login_user1(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate_user(request, username=username, password=password)
            if user is not None:
                request.session['username'] = username
                #request.session.set_expiry(0)
                return redirect("/user")
            else:
                return redirect("/login")
        else:
            return redirect("/login")
    return render(request, 'user/login.html',{'form': form})




def login_user(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # username = request.POST['username']
            # password = request.POST['password']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate_user(request, username=username, password=password)
            if user is not None:
                request.session['username'] = username
                #request.session.set_expiry(0)
                return redirect("/user")
            else:
                return redirect("/login")
    return render(request, 'user/login.html',{})


def logout_user(request):
    del request.session['username']
    return redirect("/")

def register1(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            form.save()
            return redirect("/")
            #return HttpResponse(form.is_valid())
        else:
            return HttpResponse(form.is_valid())
    return render(request, 'user/register.html',{})



def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
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
            return HttpResponse(form.is_valid())
    return render(request, 'user/register.html',{})


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
        #return redirect("/user")
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def create_ticket(request):
    if request.session.has_key('username'):
        user = Users.objects.get(username=request.session['username'])
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


def handle_uploaded_file(f):
    path = "media/photos/"+f.name
    file = open(path, 'wb+')
    for chunk in f.chunks():
        file.write(chunk)
    file.close()



class IndexView(generic.ListView):
    template_name = 'user/index.html'
    context_object_name = 'latest_user_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Users.objects.order_by('-created')


class DetailView(generic.DetailView):
    model = Users
    template_name = 'user/detail.html'