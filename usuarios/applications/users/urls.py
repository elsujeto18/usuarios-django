from django.contrib import admin
from django.core.exceptions import AppRegistryNotReady
from django.urls import path

from .views import *

app_name='users_app'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='registro'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('update-password/', UpdatePassword.as_view(), name='update-password'),
    path('user-verification/<pk>', CodeVerificationView.as_view(), name='user-verification'),
    
]
