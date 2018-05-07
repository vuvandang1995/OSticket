from django import forms
from user.models import *


class ForwardForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Text here',
            'width': 'auto',
            'height': 'auto',
        }
    ))
    # receiver = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
    #                           choices=[(x.id, x.fullname) for x in Agents.objects.all()])


class AddForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Text here',
            'width': 'auto',
            'height': 'auto',
        }
    ))
    # receiver = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
    #                           choices=[(x.id, x.fullname) for x in Agents.objects.all()])
