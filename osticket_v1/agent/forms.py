from django import forms
from user.models import *


class AddOrForwardForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Text here',
            'cols': '146',
            'rows': '20',
        }
    ))
    receiver = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                              choices=[(x.id, x.fullname) for x in Agents.objects.all()])