from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from .forms import ProfileCreateForm, LoginForm
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


class CreateProfileView(View):
    def get(self, request):
        form = ProfileCreateForm()
        context = {'form': form}
        return render(request, 'users/create_profile.html', context)

    def post(self, request):
        form = ProfileCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('УРАААААААА')
        return HttpResponse('NOOOOoooooooooooooOOOOO')
        # return render(request, 'users/create_profile.html')


class LoginPageView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'users/login.html', context={'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Hush kelibsiz' + ' ' + username)
                return redirect('profile', username)
            return HttpResponse('Not found!!!!')


class LogoutPageView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class ProfilePageView(View):
    def get(self, request, username):
        profile = get_object_or_404(Profile, username=username)
        return render(request, 'users/profile.html', context={'profile': profile})
