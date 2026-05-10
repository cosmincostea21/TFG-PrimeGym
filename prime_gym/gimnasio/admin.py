from django.contrib import admin
from .models import Tarifa, Entrenador, Clase, Cliente, Reserva

# ===========================
# TARIFAS
# ===========================
@admin.register(Tarifa)
class TarifaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'duracion_meses')
    search_fields = ('nombre',)
    list_filter = ('duracion_meses',)


# ===========================
# ENTRENADORES
# ===========================
@admin.register(Entrenador)
class EntrenadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'especialidad', 'rol')
    search_fields = ('user__username', 'user__email', 'especialidad')
    list_filter = ('rol',)

    def nombre(self, obj):
        return obj.user.username

    nombre.admin_order_field = 'user__username'
    nombre.short_description = 'Nombre'

    def email(self, obj):
        return obj.user.email

    email.admin_order_field = 'user__email'
    email.short_description = 'Email'


# ===========================
# CLASES
# ===========================
@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'horario', 'entrenador', 'capacidad')
    search_fields = ('nombre', 'descripcion', 'entrenador__nombre')
    list_filter = ('entrenador', 'tarifas')
    filter_horizontal = ('tarifas',)


# ===========================
# CLIENTES
# ===========================
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'tarifa', 'fecha_registro')
    search_fields = ('user__username', 'user__email')
    list_filter = ('tarifa', 'fecha_registro')

    def nombre(self, obj):
        return obj.user.username

    nombre.admin_order_field = 'user__username'
    nombre.short_description = 'Nombre'

    def email(self, obj):
        return obj.user.email

    email.admin_order_field = 'user__email'
    email.short_description = 'Email'


# ===========================
# RESERVAS
# ===========================
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'clase', 'fecha_reserva', 'estado')
    search_fields = ('cliente__nombre', 'clase__nombre')
    list_filter = ('estado', 'fecha_reserva', 'clase')
    date_hierarchy = 'fecha_reserva'