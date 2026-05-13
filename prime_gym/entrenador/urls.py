from django.urls import path
from . import views

app_name = "entrenador"

urlpatterns = [
    path('', views.panel_entrenador, name='panel'),
    path('mis-clases/', views.mis_clases,name='mis_clases'),
    path('clase/<int:clase_id>/reservas/', views.reservas_clase, name='reservas_clase'),
    path('reserva/<int:reserva_id>/estado/<str:estado>/', views.cambiar_estado, name = 'cambiar_estado'),
    path('clases-hoy/', views.clases_hoy, name='clases_hoy'),
    path('cambiar-password/', views.cambiar_password_entrenador, name='cambiar_password'),
    path('admin/clientes/', views.admin_clientes, name = 'admin_clientes'),
    path('admin/cliente/<int:cliente_id>/tarifa/', views.cambiar_tarifa_cliente,name = 'cambiar_tarifa_cliente'),
    path('admin/crear-entrenador/', views.crear_entrenador, name='crear_entrenador'),
    path('admin/entrenadores/', views.admin_entrenadores, name='admin_entrenadores' ),
    path('admin/entrenadores/eliminar/<int:entrenador_id>/', views.eliminar_entrenador, name='eliminar_entrenador'),
]