from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, AkexId
from .forms import ProfileCreateForm, LoginForm, ProfileChangeForm, AkexIdForm
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class CreateProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            form = ProfileCreateForm()
            context = {'form': form}
            return render(request, 'users/create_profile.html', context)
        messages.warning(request, 'Akkaunt yaratish uchun, profildan chiqing!')
        return redirect('/')

    def post(self, request):
        form = ProfileCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tabriklayman, siz royhatdan otdingiz!')
            return redirect('login')
        messages.error(request, 'Ro\'yhatdan o\'tishda hatolik yuz berdi!')
        return render(request, 'users/create_profile.html', {'form': form})


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
                messages.success(request, 'Hush kelibsiz' + ' ' + f'{username}')
                return redirect('profile', username)
            messages.warning(request, 'Topilmadi, iltimos qayta urinib ko\'ring!')
            return render(request, 'users/login.html', context={'form': form})


class LogoutPageView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Profildan chiqdingiz!')
        return redirect('login')


class ProfilePageView(LoginRequiredMixin, View):
    def get(self, request, username):
        id_button = True
        if request.user.username == username:
            profile = get_object_or_404(Profile, username=username)
            try:
                akex_id = AkexId.objects.get(username__username=username)
                if akex_id:
                    id_button = False
            except:
                None
            return render(request, 'users/profile.html', context={'profile': profile,
                                                                  'id_button': id_button})
        else:
            messages.info(request, 'Hatolik: Siz bu profilga ruhsat olmagansiz!')
            return redirect('/')


class ProfileChangePageView(LoginRequiredMixin, View):
    def get(self, request, username):
        if request.user.username == username:
            profile = get_object_or_404(Profile, username=username)
            form = ProfileChangeForm(instance=profile)
            return render(request, 'users/profile_change_form.html', context={'form': form})
        else:
            messages.info(request, 'Hatolik: Siz bu profilga ruhsat olmagansiz!')
            return redirect('/')

    def post(self, request, username):
        if request.user.username == username:
            profile = get_object_or_404(Profile, username=username)
            form = ProfileChangeForm(data=request.POST, files=request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Siz profilingizni tahrirladiz!')
                return redirect('profile', username)
            return HttpResponse("<h1>HATOLIK YUZ BERDI, QAYTA URINING</h1><hr>\n"
                                "<a href='/'>BOSH SAHIFA</a>")
        else:
            messages.info(request, 'Hatolik: Siz bu profilga ruhsat olmagansiz!')
            return redirect('/')


class AkexIdPageView(View):
    def get(self, request):
        form = AkexIdForm()
        return render(request, 'users/akex_id.html', context={'form': form})

    def post(self, request):
        form = AkexIdForm(request.POST, files=request.FILES)
        if form.is_valid():
            profile = get_object_or_404(Profile, username=request.user)
            akex_id = form.save(commit=False)
            akex_id.username = profile
            akex_id.save()
            messages.success(request, 'Arizangiz qabul qilindi, 24 soat ichida ko`rib chiqiladi!')
            return redirect('profile', profile)
        else:
            messages.error(request, 'Iltimos formani to`gri to`ldiring!')
            return render(request, 'users/akex_id.html', context={'form': form})
