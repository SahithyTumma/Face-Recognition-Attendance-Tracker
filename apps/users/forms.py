from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class NameForm(forms.Form):
    search = forms.CharField(max_length=100)
