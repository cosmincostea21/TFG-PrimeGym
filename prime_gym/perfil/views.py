from django.shortcuts import redirect, render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta, time
from django.contrib import messages
from django.db.models import Count, Q
from gimnasio.models import Cliente, Reserva, Clase
from django.contrib.auth.hashers import check_password
from .forms import UserUpdateForm, ClienteUpdateForm


# =====================================================
# NOTA IMPORTANTE (TFG)
# -----------------------------------------------------
# Mientras el sistema de autenticación no esté
# implementado, se utiliza un cliente "simulado".
# Cuando exista login, este método se sustituirá
# por el cliente asociado a la sesión.
# =====================================================

DIAS_ES = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


def proxima_sesion_clase(nombre_clase):
    """Devuelve un datetime con la próxima sesión de la clase (o None)."""
    ahora = datetime.now()
    hoy = ahora.date()
    hora_actual = ahora.time()

    HORARIOS = {
        "Movilidad":  {"dias": [0, 2], "hora": time(9, 0)},
        "Crossfit":   {"dias": [1, 3], "hora": time(19, 0)},
        "Sala Libre": {
            "dias": [0, 1, 2, 3, 4, 5],
            "hora_inicio": time(8, 0),
            "hora_fin":    time(22, 0),
        },
    }

    datos = HORARIOS.get(nombre_clase)
    if not datos:
        return None

    if nombre_clase == "Sala Libre":
        fecha = hoy + timedelta(days=1) if ahora.weekday() == 6 else hoy
        if hora_actual < datos["hora_inicio"]:
            return datetime.combine(fecha, datos["hora_inicio"])
        if hora_actual > datos["hora_fin"]:
            fecha += timedelta(days=1)
            if fecha.weekday() == 6:
                fecha += timedelta(days=1)
            return datetime.combine(fecha, datos["hora_inicio"])
        return ahora

    posibles = []
    for dia in datos["dias"]:
        offset = (dia - ahora.weekday()) % 7
        fecha_hora = datetime.combine(hoy + timedelta(days=offset), datos["hora"])
        if offset == 0 and fecha_hora <= ahora:
            fecha_hora += timedelta(days=7)
        posibles.append(fecha_hora)
    return min(posibles)


def get_cliente_actual(request):
    """
    Devuelve el cliente asociado al usuario autenticado.
    """
    if not request.user.is_authenticated:
        return None

    return get_object_or_404(Cliente, user=request.user)



# =====================================================
# DASHBOARD DEL CLIENTE
# =====================================================
@login_required
def dashboard(request):
    
    if request.user.is_staff:
        raise PermissionDenied  

    cliente = get_cliente_actual(request)

    clases = Clase.objects.all().prefetch_related('tarifas')

    # marcar disponibilidad por tarifa
    for clase in clases:
        clase.disponible = cliente.tarifa in clase.tarifas.all()

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
@login_required
def datos_personales(request):
    cliente = get_cliente_actual(request)

    context = {
        'cliente': cliente,
    }

    return render(request, 'perfil/datos_personales.html', context)

# =====================================================
# MIS RESERVAS
# =====================================================
@login_required
def mis_reservas(request):
    if request.user.is_staff:
        raise PermissionDenied  
    cliente = get_cliente_actual(request)
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
            
            hoy = date.today()

            # No se puede asistir antes de la fecha
            if reserva.fecha_reserva > hoy:
                messages.error(
                    request,
                    "No puedes marcar la asistencia antes de la fecha de la clase."
                )
                return redirect('perfil:mis_reservas')


            if reserva.estado == 'reservada':
                reserva.estado = 'asistio'
                reserva.save()
                messages.success(request, "Reserva marcada como asistida.")

            return redirect('perfil:mis_reservas')

       # ---------------------------
        # RESERVAR CLASE
        # ---------------------------
        if accion == 'reservar':
            clase = get_object_or_404(Clase, id=request.POST.get('clase_id'))

            if cliente.tarifa not in clase.tarifas.all():
                messages.error(request, "No tienes acceso a esta clase.")
                return redirect('perfil:mis_reservas')

            # 1. Calcular la fecha REAL de la próxima sesión
            proxima = proxima_sesion_clase(clase.nombre)
            if not proxima:
                messages.error(request, "No hay horario configurado para esta clase.")
                return redirect('perfil:mis_reservas')
            fecha_clase = proxima.date()
            hora_clase  = proxima.time()

            # 2. Aforo en la fecha real
            reservas_activas = Reserva.objects.filter(
                clase=clase, fecha_reserva=fecha_clase, estado='reservada'
            ).count()
            if reservas_activas >= clase.capacidad:
                messages.error(request, "La clase ha alcanzado su aforo máximo.")
                return redirect('perfil:mis_reservas')

            # 3. Reserva existente para esa fecha
            existente = Reserva.objects.filter(
                cliente=cliente, clase=clase, fecha_reserva=fecha_clase
            ).first()
            if existente:
                if existente.estado == 'reservada':
                    messages.warning(request, f"Ya tienes esta clase reservada para el {fecha_clase:%d/%m/%Y}.")
                elif existente.estado == 'cancelada':
                    messages.error(request, "Esta clase fue cancelada y no se puede volver a reservar.")
                elif existente.estado == 'asistio':
                    messages.warning(request, "Ya has asistido a esta clase.")
                return redirect('perfil:mis_reservas')

            # 4. Crear con la fecha REAL (no con hoy)
            Reserva.objects.create(
                cliente=cliente,
                clase=clase,
                fecha_reserva=fecha_clase,
                estado='reservada'
            )

            dia_es = DIAS_ES[fecha_clase.weekday()]
            messages.success(
                request,
                f"Reserva confirmada para el {dia_es} {fecha_clase:%d/%m/%Y} a las {hora_clase:%H:%M}."
            )
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

    clases_qs = (
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

    # Adjuntar la próxima sesión a cada clase para que el template la lea
    clases = []
    for clase in clases_qs:
        prox_dt = proxima_sesion_clase(clase.nombre)
        if prox_dt:
            fecha = prox_dt.date()
            clase.ocupadas = Reserva.objects.filter(
                clase=clase,
                fecha_reserva=fecha,
                estado='reservada'
            ).count()

            clase.proxima = {
                'fecha':  prox_dt.date(),
                'hora':   prox_dt.strftime("%H:%M"),
                'dia':    DIAS_ES[prox_dt.weekday()],
                'es_hoy': prox_dt.date() == hoy,
            }
        else:
            clase.ocupadas=0
            clase.proxima = None
        clases.append(clase)

    

    total_asistidas = Reserva.objects.filter(
        cliente=cliente,
        estado='asistio'
    ).count()

    context = {
        'cliente': cliente,
        'reservas': reservas,
        'clases': clases,
        'hoy': hoy,
        'total_asistidas': total_asistidas,
    }

    return render(request, 'perfil/reservas.html', context)

@login_required
def editar_perfil(request):
    # Obtenemos el perfil del cliente asociado al usuario actual
    cliente = get_object_or_404(Cliente, user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        c_form = ClienteUpdateForm(request.POST, instance=cliente)

        if u_form.is_valid() and c_form.is_valid():
            u_form.save()
            c_form.save()
            messages.success(request, "¡Tu perfil ha sido actualizado!")
            return redirect('perfil:editar_perfil') 
    else:
        u_form = UserUpdateForm(instance=request.user)
        c_form = ClienteUpdateForm(instance=cliente)

    context = {
        'u_form': u_form,
        'c_form': c_form
    }
    return render(request, 'perfil/editar_perfil.html', context)
