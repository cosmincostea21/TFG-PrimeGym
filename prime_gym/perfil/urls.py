from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'perfil'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('reservas/', views.mis_reservas, name='mis_reservas'),
]

