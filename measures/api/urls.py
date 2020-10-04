from django.conf.urls import url
from django.urls import path, include
from .views import *
from rest_framework.authtoken import views

urlpatterns = [
    path('measures/measure', MeasureAPI.as_view(), name='new_measure'),  # Crear u obtener medidas 
]
