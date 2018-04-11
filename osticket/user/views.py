from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.views import generic
from django.urls import reverse
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from .forms import *
from django.contrib import messages, auth
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
    try:
        user = Users.objects.get(pk=user_id)
    except Users.DoesNotExist:
        raise Http404("User does not exist")
    return render(request, 'user/detail.html', {'user': user})

def loginform1(request):
    if request.user.is_authenticated:
        return redirect("/")
    form = UserLoginForm()    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            #username = request.POST.get'username']
            #password = request.POST.get['password']
            #user = auth.authenticate(username=username, password= password)
            #login(request, user)
            #return redirect("/")
            #return HttpResponse(user)
            return HttpResponse(user)
        else:
            return HttpResponse(form.is_valid())
    return render(request, 'user/login.html',{'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
    return render(request, 'user/login.html',{})

def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            #print(form.cleaned_data['username'])
            form.save()
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
        return Users.objects.order_by('-created')


class DetailView(generic.DetailView):
    model = Users
    template_name = 'user/detail.html'
    