from django.conf.urls import url
from django.urls import path, include
from .views import *
from rest_framework.authtoken import views

urlpatterns = [
    path('auth/login', LoginAPI.as_view(), name='login'),                                           #Login
]
