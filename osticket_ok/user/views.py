from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import generic
from .models import *
from .forms import *


def creat_ticket(request):
    form = CreateNewTicketForm()
    return render(request, 'user/create_ticket.html',{'form': form})


def homeuser(request):
    if request.session.has_key('username'):
        print(request.session.session_key)
        user = User.objects.get(username=request.session['username'])
        return render(request, 'user/home_user.html', {'user': user})
    else:
        return redirect("/")

def detail(request):
    if request.session.has_key('username'):
        user = User.objects.get(username=request.session['username'])
        return render(request, 'user/detail.html', {'user': user})
    else:
        return redirect("/")

def login_user(request):
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
        return User.objects.order_by('-created')


class DetailView(generic.DetailView):
    model = User
    template_name = 'user/detail.html'