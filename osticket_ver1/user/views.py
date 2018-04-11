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


def index(request):
    latest_user_list = Users.objects.order_by('-created')[:5]
    context = {
        'latest_user_list': latest_user_list,
    }
    return render(request, 'user/index.html', context)

def results(request, user_id):
    response = "You're looking at the results of user %s."
    return HttpResponse(response % user_id)

def vote(request, user_id):
    return HttpResponse("You're voting on user %s." % user_id)

def detail(request, user_id):
    if request.session._session:
        user = UserUsers.objects.get(username=request.session['username'])
        # user = UserUsers.objects.get(pk=user_id)
        if user.id == user_id:
            return render(request, 'user/detail.html', {'user': user})
        else:
            return redirect("/login")
    else:
        return redirect("/login")



def login_user_goc(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate_user(request, username=username, password=password)
        if user is not None:
            return redirect("/"+str(user.id))
    return render(request, 'user/login.html',{})


def login_user(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate_user(request, username=username, password=password)
            print(username, password)
            if user is not None:
                request.session['username'] = username
                return redirect("/"+str(user.id))
            else:
                form = UserLoginForm()
        else:
            #form = UserLoginForm()
            print(form.is_valid())
    return render(request, 'user/login.html',{'form': form})

def logout_user(request):
    del request.session['username']
    return redirect("/login")

def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #sdt = form.cleaned_data['sdt']
            #print(form.cleaned_data['username'])
            form.save()
            #user = User.objects.create_user(username, sdt=sdt, password=password)
            #return redirect("/")
            #return HttpResponse(form.is_valid())
        else:
            return HttpResponse(form.is_valid())
    return render(request, 'user/register.html',{'form': form})

class IndexView(generic.ListView):
    template_name = 'user/index.html'
    context_object_name = 'latest_user_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return UserUsers.objects.order_by('-created')


class DetailView(generic.DetailView):
    model = UserUsers
    template_name = 'user/detail.html'