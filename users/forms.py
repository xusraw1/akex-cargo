from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile, AkexId


class ProfileCreateForm(UserCreationForm):
    error_messages = {
        'username': {
            'required': "Majburiy. 150 yoki undan kam belgi. Faqat harflar, raqamlar va @/./+/-/_. Boshqa shaxsiy ma'lumotlaringizga juda o'xshash bo'lishi mumkin emas.",
        },
        'password1': {
            'required': "Parolingiz kamida 8 ta belgidan iborat bo'lishi kerak.",
            'password_too_short': "Parolingiz kamida 8 ta belgidan iborat bo'lishi kerak.",
            'password_common': "Sizning parolingiz keng tarqalgan parol bo'lishi mumkin emas.",
            'password_entirely_numeric': "Parolingiz to'liq raqamli bo'lishi mumkin emas.",
        }
    }

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Username',
            'first_name': 'Ism',
            'last_name': 'Familiya',
            'email': 'Email-Manzil',
        }

    def __init__(self, *args, **kwargs):
        super(ProfileCreateForm, self).__init__(*args, **kwargs)
        self.fields['username'].error_messages = {
            'required': "Majburiy. 150 yoki undan kam belgi. Faqat harflar, raqamlar va @/./+/-/_. Boshqa shaxsiy ma'lumotlaringizga juda o'xshash bo'lishi mumkin emas.",
        }
        self.fields['password1'].error_messages = {
            'required': "Parolingiz kamida 8 ta belgidan iborat bo'lishi kerak.",
            'password_too_short': "Parolingiz kamida 8 ta belgidan iborat bo'lishi kerak.",
            'password_common': "Sizning parolingiz keng tarqalgan parol bo'lishi mumkin emas.",
            'password_entirely_numeric': "Parolingiz to'liq raqamli bo'lishi mumkin emas.",
        }


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


class ProfileAndPasswordChangeForm(forms.Form):
    old_password = forms.CharField(label='Eski parol', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='Yangi parol', widget=forms.PasswordInput, min_length=8)
    new_password2 = forms.CharField(label='Yangi parolni tasdiqlash', widget=forms.PasswordInput, min_length=8)
