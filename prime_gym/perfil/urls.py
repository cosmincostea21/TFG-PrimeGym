from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'perfil'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('datos/', views.datos_personales, name='datos_personales'),
    path('reservas/', views.mis_reservas, name='mis_reservas'),
]

