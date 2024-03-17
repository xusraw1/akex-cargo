from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, AkexId
from .forms import ProfileCreateForm, LoginForm, ProfileChangeForm, AkexIdForm, ProfileAndPasswordChangeForm
from django.views import View
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash


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
            print(username)
            print(password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Hush kelibsiz' + ' ' + f'{username}')
                return redirect('profile', username)
            messages.warning(request, 'Topilmadi, iltimos qayta urinib ko\'ring!')
            return render(request, 'users/login.html', context={'form': form})
        messages.error(request, 'Formani to`ldirishda hatolik yuz berdi!')
        return render(request, 'users/login.html', context={'form': form})


class LogoutPageView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Profildan chiqdingiz!')
        return redirect('login')


class ProfilePageView(LoginRequiredMixin, View):
    def get(self, request, username):
        id_button = True
        context = {'id_button': True}
        if request.user.username == username:
            profile = get_object_or_404(Profile, username=username)
            context['profile'] = profile
            try:
                akex_id = AkexId.objects.get(username__username=username)
                if akex_id:
                    id_button = False
                    context['id_button'] = False
                    context['akex'] = akex_id
            except:
                None
            return render(request, 'users/profile.html', context)
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


class AkexIdPageView(LoginRequiredMixin, View):
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


class SuperUser(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseForbidden("Faqatgina SUPERUSER kiraoladi!")

    def get(self, request):
        given = request.GET.get('given')
        requests = request.GET.get('requests')
        akex_users = AkexId.objects.filter(status=False) if requests else None
        profile = Profile.objects.filter(akex_id__isnull=False) if given else None
        context = {'akex_users': akex_users, 'profile': profile}
        return render(request, 'users/akex_id_list.html', context)


class IdCheck(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseForbidden("Faqatgina SUPERUSER kiraoladi!")

    def get(self, request, username):
        akex = get_object_or_404(AkexId, username__username=username)
        context = {'akex': akex}
        return render(request, 'users/akex_id_check.html', context)

    def post(self, request, username):
        accept = request.POST.get('accept')
        rejected = request.POST.get('reject')
        text = request.POST.get('id')
        address = request.POST.get('address')
        user = request.POST.get('username')
        print(text)
        if accept != None:
            profile = get_object_or_404(Profile, username=user)
            profile.akex_id = text
            profile.akex_address = address
            akex = get_object_or_404(AkexId, username__username=user)
            akex.status = True
            akex.save()
            profile.save()
            messages.success(request, 'ID berildi!')
            return redirect('id_berish')
        elif rejected != None:
            akex = get_object_or_404(AkexId, username__username=user)
            akex.delete()
            messages.success(request, 'Qayta topshirish yangilandi!')
            return redirect('id_berish')
        else:
            return HttpResponseBadRequest("Invalid request")


class IdChange(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseForbidden("Faqatgina SUPERUSER kiraoladi!")

    def get(self, request, username):
        akex = AkexId.objects.select_related('username').get(username__username=username)
        context = {'akex': akex}
        return render(request, 'users/akex_id_change.html', context)

    def post(self, request, username):
        accept = request.POST.get('accept')
        rejected = request.POST.get('reject')
        text = request.POST.get('id')
        address = request.POST.get('address')
        user = request.POST.get('username')
        print(text)
        if accept != None:
            profile = get_object_or_404(Profile, username=user)
            profile.akex_id = text
            profile.akex_address = address
            akex = get_object_or_404(AkexId, username__username=user)
            akex.status = True
            akex.save()
            profile.save()
            messages.info(request, 'ID muvoffaqiyatli o`zgartirildi!')
            return redirect('id_berish')
        elif rejected != None:
            akex = get_object_or_404(AkexId, username__username=user)
            profile = get_object_or_404(Profile, username=user)
            profile.akex_id = ''
            profile.akex_address = ''
            akex.delete()
            profile.save()
            messages.warning(request, 'Uchirib tashlandi!')
            return redirect('id_berish')
        else:
            return HttpResponseBadRequest("Invalid request")


class PasswordChangeView(View):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        form = ProfileAndPasswordChangeForm()
        context = {'form': form}
        return render(request, 'users/registration/password_change_form.html', context)

    def post(self, request, username):
        user = get_object_or_404(User, username=username)
        form = ProfileAndPasswordChangeForm(data=request.POST)
        if form.is_valid():
            old_pass = form.cleaned_data['old_password']
            if user.check_password(old_pass):
                pass1 = form.cleaned_data['new_password1']
                pass2 = form.cleaned_data['new_password2']
                if pass1 == pass2:
                    user.set_password(pass1)
                    update_session_auth_hash(request, user)
                    user.save()
                    messages.success(request, 'Parol o`zgardi!')
                    return redirect('profile', username)
                messages.warning(request, 'Yangi parollardan biri hato kiritildi, iltimos qayta urinib ko`ring!')
                return redirect('password_change', username)
            else:
                messages.warning(request, 'Eski parol hato kiritildi!')
                return redirect('password_change', username)
        else:
            messages.info(request, 'Formani to`gri to`ldiring, iltimos!')
            return redirect('password_change', username)
