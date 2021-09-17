from django.contrib import admin
from django.urls import path

from .views import *


app_name= 'home_app'
urlpatterns = [
    path('home/', Homepage.as_view(), name='home'),
]