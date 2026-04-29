from django.urls import path
from . import views

app_name = "entrenador"

urlpatterns = [
    path('', views.panel_entrenador, name='panel'),
    path('mis-clases/', views.mis_clases,name='mis_clases'),
    path('clase/<int:clase_id>/reservas/', views.reservas_clase, name='reservas_clase'),
    path('asistencia/<int:reserva_id>/', views.marcar_asistencia, name='marcar_asistencia'),
    path('clases-hoy/', views.clases_hoy, name='clases_hoy'),
]