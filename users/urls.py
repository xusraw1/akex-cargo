from django.urls import path
from .views import *
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordChangeDoneView, \
    PasswordResetCompleteView

urlpatterns = [
    path('create-profile/', CreateProfileView.as_view(), name='create_profile'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('logout/', LogoutPageView.as_view(), name='logout'),
    path('profile/<str:username>/', ProfilePageView.as_view(), name='profile'),
    path('profile-change/<str:username>/', ProfileChangePageView.as_view(), name='profile_change_form'),
    path('akex-id/', AkexIdPageView.as_view(), name='akex_id'),
    path('akex-id-berish/', SuperUser.as_view(), name='id_berish'),
    path('akex-id-chek/<str:username>/', IdCheck.as_view(), name='id_chek'),
    path('akex-id-change/<str:username>/', IdChange.as_view(), name='id_change'),

    # password change
    path('change-password/<str:username>/', PasswordChangeView.as_view(), name='password_change'),

    path('password-reset/', CustomPasswordResetView.as_view(), name='reset_password'),

    path('password-reset/done/', PasswordChangeDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),

    path('password-reset/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='reset_password_confirm'),

    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
