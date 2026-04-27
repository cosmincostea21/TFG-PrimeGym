from django.shortcuts import render, get_object_or_404
from datetime import date
from gimnasio.models import Cliente, Reserva, Clase, Tarifa


# =====================================================
# NOTA IMPORTANTE (TFG)
# -----------------------------------------------------
# Mientras el sistema de autenticación no esté
# implementado, se utiliza un cliente "simulado".
# Cuando exista login, este método se sustituirá
# por el cliente asociado a la sesión.
# =====================================================

def get_cliente_actual():
    """
    Devuelve un cliente temporal para desarrollo.
    En el futuro se sustituirá por el cliente
    asociado a la sesión.
    """
    return Cliente.objects.first()


# =====================================================
# DASHBOARD DEL CLIENTE
# =====================================================
def dashboard(request):
    cliente = get_cliente_actual()

    reservas = cliente.reservas.all().order_by('fecha_reserva')

    proxima_reserva = reservas.filter(
        fecha_reserva__gte=date.today(),
        estado='reservada'
    ).first()

    ultima_asistencia = reservas.filter(
        estado='asistio'
    ).order_by('-fecha_reserva').first()


    context = {
        'cliente': cliente,
        'tarifa': cliente.tarifa,
        'num_reservas': reservas.count(),
        'proxima_reserva': proxima_reserva,
        'ultima_asistencia': ultima_asistencia,
    }

    return render(request, 'perfil/dashboard.html', context)


# =====================================================
# DATOS PERSONALES
# =====================================================
def datos_personales(request):
    cliente = get_cliente_actual()

    context = {
        'cliente': cliente,
    }

    return render(request, 'perfil/datos_personales.html', context)


# =====================================================
# MIS RESERVAS
# =====================================================
def mis_reservas(request):
    cliente = get_cliente_actual()

    reservas = (
        Reserva.objects
        .filter(cliente=cliente)
        .select_related('clase')
        .order_by('-fecha_reserva')
    )

    context = {
        'cliente': cliente,
        'reservas': reservas,
    }

    return render(request, 'perfil/reservas.html', context)


# =====================================================
# CLASES DISPONIBLES SEGÚN TARIFA
# =====================================================
def clases_disponibles(request):
    cliente = get_cliente_actual()

    clases = Clase.objects.filter(tarifas=cliente.tarifa).select_related('entrenador')

    context = {
        'cliente': cliente,
        'clases': clases,
    }

    return render(request, 'perfil/clases.html', context)


# =====================================================
# CAMBIAR TARIFA (VERSIÓN SIMPLE)
# =====================================================
def cambiar_tarifa(request):
    cliente = get_cliente_actual()
    tarifas = Tarifa.objects.all()

    if request.method == 'POST':
        tarifa_id = request.POST.get('tarifa_id')
        tarifa = get_object_or_404(Tarifa, id=tarifa_id)
        cliente.tarifa = tarifa
        cliente.save()

    context = {
        'cliente': cliente,
        'tarifas': tarifas,
    }

    return render(request, 'perfil/cambiar_tarifa.html', context)
