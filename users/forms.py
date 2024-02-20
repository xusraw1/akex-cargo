from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile, AkexId


class ProfileCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput, label='Parol')


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'telegram', 'phone', 'avatar', 'address']


class AkexIdForm(forms.ModelForm):
    class Meta:
        model = AkexId
        fields = ['pinfl', 'sp', 'image']
