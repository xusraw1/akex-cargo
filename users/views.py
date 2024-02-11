from django.shortcuts import render, redirect
from .models import Profile
from .forms import ProfileCreateForm, LoginForm
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout


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
                return HttpResponse('Oh, you lucky man!')
            return HttpResponse('Not found!!!!')
