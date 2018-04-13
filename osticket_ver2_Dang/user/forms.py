from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate, login
from user.models import *
from django.utils import timezone

class RegistrationForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(
        attrs={               
            'class': 'form-control',
            'placeholder': 'Full name',
        }
    ))

    username = forms.CharField(widget=forms.TextInput(
        attrs={               
            'class': 'form-control',
            'placeholder': 'User name',
        }
    ))

    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    })
    )

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={               
            'class': 'form-control',
            'placeholder': 'Password',
        }
    ))

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={               
            'class': 'form-control',
            'placeholder': 'Password',
        }
    ))

    def clean_password2(self):
        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            password2 = self.cleaned_data['password2']
            if password == password2 and password:
                return password2
        raise forms.ValidationError("Mật khẩu không hợp lệ")


    def clean_username(self):
        username =  self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError("Tài khoản đã tồn tại")
    
    def save(self):
        u = Users(fullname=self.cleaned_data['fullname'], username=self.cleaned_data['username'], email=self.cleaned_data['email'], password=self.cleaned_data['password'], created=timezone.now())
        u.save()
        return u

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={               
            'class': 'form-control',
            'placeholder': 'User name',
        }
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={               
            'class': 'form-control',
            'placeholder': 'Password',
        }
    ))


    def clean_username(self):
        username =  self.cleaned_data['username']
        return username

class CreateNewTicketForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'title',
        }
    ))
    topic = forms.ChoiceField(choices=[(x.id,x.name) for x in Topics.objects.all()])

    content = forms.CharField(widget=forms.Textarea(attrs={
        'cols': '146',
        'rows': '20',
        'class': 'form-control',
        'placeholder': 'content',
    })
    )

    attach = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control',
        'placeholder': 'attach',
    })
    )