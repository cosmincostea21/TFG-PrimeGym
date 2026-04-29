from datetime import date
from django.shortcuts import render, redirect
from gimnasio.models import Clase, Reserva, Entrenador

# Create your views here.

# VER CLASES ENTRENADOR
def mis_clases(request):
    #entrenador = Entrenador.objects.get(email=request.user.email)
    entrenador = Entrenador.objects.first()
    clases = Clase.objects.filter(entrenador=entrenador)

    return render(request, 'entrenador/mis_clases.html', {'clases': clases})

# VER RESERVAS EN CLASES ENTRENADOR
def reservas_clase(request, clase_id):
    clase = Clase.objects.get(id=clase_id)
    reservas = Reserva.objects.filter(clase=clase)

    return render(request, 'entrenador/reservas_clase.html', {'clase': clase, 'reservas': reservas})

# EDITAR ASISTENCIA
def marcar_asistencia(request, reserva_id):
    reserva = Reserva.objects.get(id=reserva_id)
    reserva.estado = 'asistio'
    reserva.save()

    return redirect('entrenador:mis_clases')

# PANEL DEL ENTRENADOR
def panel_entrenador(request):
    #entrenador = Entrenador.objects.get(email=request.user.email)
    entrenador = Entrenador.objects.first()
    clases = Clase.objects.filter(entrenador=entrenador)
    total_clases = clases.count()

    total_reservas = Reserva.objects.filter(clase__entrenador=entrenador).count()

    hoy = date.today()
    clases_hoy = Reserva.objects.filter(clase__entrenador=entrenador, fecha_reserva=hoy)

    context = {
        'total_clases': total_clases,
        'total_reservas': total_reservas,
        'clases_hoy': clases_hoy
    }

    return render(request, 'entrenador/panel.html', context)

# CLASES DEL DIA
def clases_hoy(request):
    #entrenador = Entrenador.objects.get(email=request.user.email)
    entrenador = Entrenador.objects.first()
    hoy = date.today()
    reservas_hoy = Reserva.objects.filter(clase__entrenador=entrenador, fecha_reserva=hoy)

    return render(request, 'entrenador/clases_hoy.html', {'reservas': reservas_hoy})