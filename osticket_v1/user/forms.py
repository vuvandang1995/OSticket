from django import forms
from user.models import *
from django.utils import timezone
from django.core.validators import validate_email


# form User đăng kí tài khoản
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

    phone = forms.CharField(widget=forms.TextInput(
        attrs={               
            'class': 'form-control',
            'placeholder': 'Your phone number',
        }
    ))

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

    # check password
    def clean_password2(self):
        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            password2 = self.cleaned_data['password2']
            if password == password2 and password:
                return password2
            else:
                raise forms.ValidationError("Mật khẩu không hợp lệ")
        raise forms.ValidationError("Mật khẩu không hợp lệ")


    # check xem user name đã tồn tại hay chưa
    def clean_username(self):
        username =  self.cleaned_data['username']
        if get_user(username) is not None:
            raise forms.ValidationError("Tài khoản đã tồn tại")
        return username

    # check email có đúng định dạng không, đã tồn tại chưa
    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_email(email) is not None:
            raise forms.ValidationError("Email đã được đăng kí")
        try:
            validate_email(email)
        except:
            raise forms.ValidationError("Email không hợp lệ")
        return email


    # lưu tài khoản User
    def save(self):
        u = Users(fullname=self.cleaned_data['fullname'], username=self.cleaned_data['username'], email=self.cleaned_data['email'], phone=self.cleaned_data['phone'], password=self.cleaned_data['password'], created=timezone.now())
        u.save()
        return u


# form reset mật khẩu cho User
class UserResetForm(forms.Form):
    uemail = forms.CharField(widget=forms.TextInput(
        attrs={               
            'class': 'form-control',
            'placeholder': 'email',
        }
    ))

    # check email xem đã tồn tại chưa, đúng định dạng không
    def clean_uemail(self):
        uemail = self.cleaned_data['uemail']
        if get_user_email(uemail) is None:
            raise forms.ValidationError("Email đã chưa được đăng kí")
        try:
            validate_email(uemail)
        except:
            raise forms.ValidationError("Email không hợp lệ")
        return uemail


# form thay đổi mật khẩu mới khi User bấm vào link xác nhận trong email
class ResetForm(forms.Form):
    pwd1 = forms.CharField(widget=forms.PasswordInput(
        attrs={               
            'class': 'form-control',
            'placeholder': 'Password',
        }
    ))

    pwd2 = forms.CharField(widget=forms.PasswordInput(
        attrs={               
            'class': 'form-control',
            'placeholder': 'Password',
        }
    ))

    # check mật khẩu 
    def clean(self):
        if 'pwd1' in self.cleaned_data:
            pwd1 = self.cleaned_data['pwd1']
            pwd2 = self.cleaned_data['pwd2']
            if pwd1 == pwd2 and pwd1:
                return pwd1
            else:
                raise forms.ValidationError("Mật khẩu không hợp lệ")
        raise forms.ValidationError("Mật khẩu không hợp lệ")
    
    
# form User đăng nhập
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

    # check xem tài khoản có tồn tại không
    def clean(self):
        if 'username' in self.cleaned_data:
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if authenticate_user(username=username, password=password) is None:
                raise forms.ValidationError('')


# form Agent đăng nhập
class AgentLoginForm(forms.Form):
    agentname = forms.CharField(widget=forms.TextInput(
        attrs={               
            'class': 'form-control',
            'placeholder': 'User name',
        }
    ))

    agentpass = forms.CharField(widget=forms.PasswordInput(
        attrs={               
            'class': 'form-control',
            'placeholder': 'Password',
        }
    ))


# form tạo tịcket
class CreateNewTicketForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'title',
        }
    ))
    topic = forms.ChoiceField(choices=[(x.id,x.name) for x in Topics.objects.all()])

    content = forms.CharField(widget=forms.Textarea(attrs={
        'cols': '100',
        'rows': '20',
        'class': 'form-control',
        'placeholder': 'content',
    })
    )

    attach = forms.FileField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control',
        'placeholder': 'attach',
        'id': 'i_file',
    })
    )


class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'comment here',
        'name':'content',
    }))
