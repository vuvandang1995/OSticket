from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.shortcuts import get_object_or_404, render
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

def register(request):
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
    return render(request, 'user/register.html',{'form': form})

class IndexView(generic.ListView):
    template_name = 'user/index.html'
    context_object_name = 'latest_user_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Users.objects.order_by('-created')


class DetailView(generic.DetailView):
    model = Users
    template_name = 'user/detail.html'