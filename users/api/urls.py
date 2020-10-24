from django.conf.urls import url
from django.urls import path, include
from .views import *
from rest_framework.authtoken import views
from knox import views as knox_views

urlpatterns = [
    path('auth', include('knox.urls')),  # Autenticación
    path('auth/login', LoginAPI.as_view(), name='login'),  #Login
    path('users/get-all', UsersDoctorAPI.as_view(), name='get_all_users'),  # Obtengo todos los usuarios de un doctor

]
