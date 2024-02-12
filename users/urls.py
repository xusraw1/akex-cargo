from django.urls import path
from .views import *

urlpatterns = [
    path('create-profile/', CreateProfileView.as_view(), name='create_profile'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('logout/', LogoutPageView.as_view(), name='logout'),
    path('profile/<str:username>/', ProfilePageView.as_view(), name='profile'),
]