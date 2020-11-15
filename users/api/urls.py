from django.conf.urls import url
from django.urls import path, include
from .views import *
from rest_framework.authtoken import views
from knox import views as knox_views

urlpatterns = [
    path('auth', include('knox.urls')),                                         #Autenticación
    path('auth/login', LoginAPI.as_view(), name='login'),                       #Login
    path('auth/register', RegisterAPI.as_view(), name='register'),              #Register
    path('users/get-all', UsersDoctorAPI.as_view(), name='get_all_users'),      #Obtengo todos los usuarios de un doctor
    path('users/patient', PatientDataAPI.as_view(), name='get_patient_data'),   #Obtengo los datos de un paciente
    path('users/doctors', DoctorsAPI.as_view(), name='get_doctors'),            #Obtener todos los doctores
]
