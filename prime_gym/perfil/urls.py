from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views),
    path('datos/', views),
    path('reservas/', views),
    path('tarifa/', views),
]
