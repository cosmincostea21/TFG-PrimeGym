from datetime import date, datetime, timedelta, time
from django.shortcuts import render, redirect, get_object_or_404
from gimnasio.models import Clase, Reserva, Entrenador, Cliente, Tarifa
from .decorators import admin_required

# Create your views here.

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


def sesiones_anteriores_clase(nombre_clase, n=2):
    """Devuelve las fechas de las N sesiones pasadas más recientes de la clase."""
    ahora = datetime.now()
    hoy   = ahora.date()

    HORARIOS = {
        "Movilidad":  {"dias": [0, 2], "hora": time(9, 0)},
        "Crossfit":   {"dias": [1, 3], "hora": time(19, 0)},
        "Sala Libre": {"dias": [0, 1, 2, 3, 4, 5], "hora_inicio": time(8, 0)},
    }
    datos = HORARIOS.get(nombre_clase)
    if not datos:
        return []

    hora_ref = datos.get("hora") or datos.get("hora_inicio")
    fechas = []

    # Recorremos hacia atrás día por día hasta tener N sesiones pasadas
    dia_cursor = hoy
    limite = 0
    while len(fechas) < n and limite < 60:        # tope de 60 días por seguridad
        if dia_cursor.weekday() in datos["dias"]:
            fecha_hora = datetime.combine(dia_cursor, hora_ref)
            # Solo cuenta si ya ha ocurrido (fecha pasada o misma fecha con hora pasada)
            if fecha_hora < ahora:
                fechas.append(dia_cursor)
        dia_cursor -= timedelta(days=1)
        limite += 1

    return fechas


# VER CLASES ENTRENADOR
def mis_clases(request):
    #entrenador = Entrenador.objects.get(email=request.user.email)
    entrenador = Entrenador.objects.first()
    clases = Clase.objects.filter(entrenador=entrenador)

    return render(request, 'entrenador/mis_clases.html', {'clases': clases})

# VER RESERVAS EN CLASES ENTRENADOR
def reservas_clase(request, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)

    # Próxima sesión
    proxima_dt    = proxima_sesion_clase(clase.nombre)
    fecha_proxima = proxima_dt.date() if proxima_dt else None

    # 2 sesiones anteriores (la más reciente primero)
    fechas_anteriores = sesiones_anteriores_clase(clase.nombre, n=2)
    fecha_ant_1 = fechas_anteriores[0] if len(fechas_anteriores) > 0 else None
    fecha_ant_2 = fechas_anteriores[1] if len(fechas_anteriores) > 1 else None

    # Construimos las opciones del filtro (clave = ISO date, valor = etiqueta)
    opciones = []
    if fecha_proxima:
        opciones.append({
            'value': fecha_proxima.isoformat(),
            'label': f"Próxima · {DIAS_ES[fecha_proxima.weekday()]} {fecha_proxima:%d/%m}",
            'fecha': fecha_proxima,
            'tipo':  'proxima',
        })
    if fecha_ant_1:
        opciones.append({
            'value': fecha_ant_1.isoformat(),
            'label': f"Anterior · {DIAS_ES[fecha_ant_1.weekday()]} {fecha_ant_1:%d/%m}",
            'fecha': fecha_ant_1,
            'tipo':  'anterior_1',
        })
    if fecha_ant_2:
        opciones.append({
            'value': fecha_ant_2.isoformat(),
            'label': f"Anterior · {DIAS_ES[fecha_ant_2.weekday()]} {fecha_ant_2:%d/%m}",
            'fecha': fecha_ant_2,
            'tipo':  'anterior_2',
        })

    # Fecha seleccionada (default = próxima)
    fecha_sel_iso = request.GET.get('fecha') or (opciones[0]['value'] if opciones else None)
    fecha_sel = None
    if fecha_sel_iso:
        try:
            fecha_sel = date.fromisoformat(fecha_sel_iso)
        except ValueError:
            fecha_sel = fecha_proxima

    # Filtrado de reservas
    reservas = Reserva.objects.filter(clase=clase).select_related('cliente')
    if fecha_sel:
        reservas = reservas.filter(fecha_reserva=fecha_sel).order_by('cliente__nombre')
    else:
        reservas = reservas.none()

    # Filtro por estado
    estado = request.GET.get('estado')
    if estado and estado != 'todos':
        reservas = reservas.filter(estado=estado)

    # Info para cabecera
    info = None
    if fecha_sel:
        es_proxima = (fecha_sel == fecha_proxima)
        info = {
            'titulo': 'Próxima sesión' if es_proxima else 'Sesión anterior',
            'dia':    DIAS_ES[fecha_sel.weekday()],
            'fecha':  fecha_sel,
            'hora':   proxima_dt.strftime("%H:%M") if (es_proxima and proxima_dt) else None,
        }

    context = {
        'clase':       clase,
        'reservas':    reservas,
        'opciones':    opciones,
        'fecha_sel':   fecha_sel_iso,
        'info':        info,
    }
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
    entrenador = Entrenador.objects.first()
    clases = Clase.objects.filter(entrenador=entrenador)

    total_clases   = clases.count()
    total_reservas = Reserva.objects.filter(clase__entrenador=entrenador).count()

    # Para cada clase calculamos su PRÓXIMA sesión + reservas activas
    proximas = []
    for clase in clases:
        prox_dt = proxima_sesion_clase(clase.nombre)
        if not prox_dt:
            continue

        fecha = prox_dt.date()
        reservas_clase = (
            Reserva.objects
            .filter(clase=clase, fecha_reserva=fecha, estado='reservada')
            .select_related('cliente')
            .order_by('cliente__nombre')
        )

        proximas.append({
            'clase':     clase,
            'fecha':     fecha,
            'hora':      prox_dt.strftime("%H:%M"),
            'dia':       DIAS_ES[fecha.weekday()],
            'es_hoy':    fecha == date.today(),
            'reservas':  reservas_clase,
            'inscritos': reservas_clase.count(),
        })

    # Ordenamos por fecha+hora para que la más cercana salga primero
    proximas.sort(key=lambda p: (p['fecha'], p['hora']))

    context = {
        'total_clases':   total_clases,
        'total_reservas': total_reservas,
        'proximas':       proximas,
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