from django.shortcuts import redirect, render, get_object_or_404
from datetime import date, datetime, timedelta
from django.contrib import messages
from django.db.models import Count, Q
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

    clases = Clase.objects.filter(tarifas=cliente.tarifa)

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
        'clases': clases,
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
    hoy = date.today()

    # ===========================
    # PROCESAR ACCIONES (POST)
    # ===========================
    if request.method == 'POST':
        accion = request.POST.get('accion', 'reservar')

        # ---------------------------
        # CANCELAR RESERVA
        # ---------------------------
        if accion == 'cancelar':
            reserva = get_object_or_404(
                Reserva,
                id=request.POST.get('reserva_id'),
                cliente=cliente
            )

            if reserva.estado == 'reservada':
                reserva.estado = 'cancelada'
                reserva.save()
                messages.success(request, "Reserva cancelada correctamente.")

            return redirect('perfil:mis_reservas')

        # ---------------------------
        # MARCAR ASISTENCIA
        # ---------------------------
        if accion == 'asistir':
            reserva = get_object_or_404(
                Reserva,
                id=request.POST.get('reserva_id'),
                cliente=cliente
            )

            if reserva.estado == 'reservada':
                reserva.estado = 'asistio'
                reserva.save()
                messages.success(request, "Reserva marcada como asistida.")

            return redirect('perfil:mis_reservas')

       # ---------------------------
        # RESERVAR CLASE
        # ---------------------------
        if accion == 'reservar':
            clase = get_object_or_404(
                Clase,
                id=request.POST.get('clase_id')
            )

            # 1️⃣ Comprobar tarifa
            if cliente.tarifa not in clase.tarifas.all():
                messages.error(request, "No tienes acceso a esta clase.")
                return redirect('perfil:mis_reservas')

            # 2️⃣ Comprobar aforo
            reservas_activas = Reserva.objects.filter(
                clase=clase,
                fecha_reserva=hoy,
                estado='reservada'
            ).count()

            if reservas_activas >= clase.capacidad:
                messages.error(request, "La clase ha alcanzado su aforo máximo.")
                return redirect('perfil:mis_reservas')

            # 3️⃣ Comprobar reserva existente
            reserva_existente = Reserva.objects.filter(
                cliente=cliente,
                clase=clase,
                fecha_reserva=hoy
            ).first()

            if reserva_existente:
                if reserva_existente.estado == 'reservada':
                    messages.warning(request, "Ya tienes esta clase reservada.")
                elif reserva_existente.estado == 'cancelada':
                    messages.error(request, "Esta clase fue cancelada y no se puede volver a reservar.")
                elif reserva_existente.estado == 'asistio':
                    messages.warning(request, "Ya has asistido a esta clase.")
                return redirect('perfil:mis_reservas')

            # 4️⃣ Crear reserva
            Reserva.objects.create(
                cliente=cliente,
                clase=clase,
                fecha_reserva=hoy,
                estado='reservada'
            )

            messages.success(request, "Clase reservada correctamente.")
            return redirect('perfil:mis_reservas')
    # ===========================
    # GET → MOSTRAR DATOS
    # ===========================
    reservas = (
        Reserva.objects
        .filter(cliente=cliente)
        .select_related('clase')
        .order_by('-fecha_reserva')
    )

    clases = (
        Clase.objects
        .filter(tarifas=cliente.tarifa)
        .annotate(
            ocupadas=Count(
                'reservas',
                filter=Q(
                    reservas__estado='reservada',
                    reservas__fecha_reserva=hoy
                )
            )
        )
    )

    context = {
        'cliente': cliente,
        'reservas': reservas,
        'clases': clases,
        'hoy': hoy,
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
