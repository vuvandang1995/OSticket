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

