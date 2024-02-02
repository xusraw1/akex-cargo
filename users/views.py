from django.shortcuts import render, redirect
from .models import Profile
from .forms import ProfileCreateForm
from django.views import View
from django.http import HttpResponse


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
