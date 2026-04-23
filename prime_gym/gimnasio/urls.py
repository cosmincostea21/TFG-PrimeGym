from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('clases/', views.clases, name='clases'),
    path('tarifas/', views.tarifas, name='tarifas'),
    path('equipo/', views.equipo, name='equipo'),
    path('contacto/', views.contacto, name='contacto'),
]
