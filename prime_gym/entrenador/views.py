from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from gimnasio.models import Clase, Reserva, Entrenador, Cliente, Tarifa
from .decorators import admin_required

# Create your views here.

# VER CLASES ENTRENADOR
def mis_clases(request):
    #entrenador = Entrenador.objects.get(email=request.user.email)
    entrenador = Entrenador.objects.first()
    clases = Clase.objects.filter(entrenador=entrenador)

    return render(request, 'entrenador/mis_clases.html', {'clases': clases})

# VER RESERVAS EN CLASES ENTRENADOR
def reservas_clase(request, clase_id):

    clase = Clase.objects.get(id = clase_id)
    reservas = Reserva.objects.filter(clase = clase)

    # FILTRO DE FECHAS
    tipo = request.GET.get('tipo')
    hoy = date.today()

    if tipo == 'hoy':
        reservas = reservas.filter(fecha_reserva = hoy)
    elif tipo == 'anteriores':
        reservas = reservas.filter(fecha_reserva__lt = hoy).order_by('-fecha_reserva')[:2]
    elif tipo == 'siguientes':
        reservas = reservas.filter(fecha_reserva__gt = hoy).order_by('fecha_reserva')[:2]

    # FILTRO DE ESTADO
    estado = request.GET.get('estado')
    if estado and estado != 'todos':
        reservas = reservas.filter(estado = estado)

    context = {'clase': clase, 'reservas': reservas}

    return render(request, 'entrenador/reservas_clase.html', context)

# EDITAR ASISTENCIA
def cambiar_estado(request, reserva_id, estado):

    reserva = get_object_or_404(Reserva, id=reserva_id)
    estados_validos = ['reservada', 'asistio', 'cancelada']

    if estado in estados_validos:
        reserva.estado = estado
        reserva.save()

    return redirect('entrenador:reservas_clase', clase_id=reserva.clase.id)

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
    reservas_hoy = Reserva.objects.filter(clase__entrenador=entrenador, fecha_reserva=hoy, estado="reservada")

    return render(request, 'entrenador/clases_hoy.html', {'reservas': reservas_hoy})

# PANEL ADMIN
@admin_required
def admin_clientes(request):
    clientes = Cliente.objects.all()
    tarifas = Tarifa.objects.all()

    query = request.GET.get("q")

    if query:
        clientes = clientes.filter(nombre__icontains=query)

    return render(request, "entrenador/admin_clientes.html", {"clientes": clientes, "tarifas": tarifas})

# ACTIVAR/DESACTIVAR CLIENTE
@admin_required
def cambiar_tarifa_cliente(request, cliente_id):

    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == "POST":
        tarifa_id = request.POST.get("tarifa")

        if not tarifa_id:
            cliente.tarifa = None
        else:
            cliente.tarifa_id = tarifa_id

        cliente.save()

    return redirect('entrenador:admin_clientes')