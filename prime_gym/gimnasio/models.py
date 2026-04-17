from django.db import models

# ===========================
# TARIFAS
# ===========================
class Tarifa(models.Model):

    nombre = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_meses = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.nombre

# ===========================
# ENTRENADORES
# ===========================
class Entrenador(models.Model):

    ROLES = [
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
    ]
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    especialidad = models.CharField(max_length=100)
    rol = models.CharField(max_length=10, choices=ROLES, default='empleado')
    password = models.CharField(max_length=255)
    def __str__(self):
        return self.nombre

# ===========================
# CLASES
# ===========================
class Clase(models.Model):

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    horario = models.CharField(max_length=50)
    entrenador = models.ForeignKey(Entrenador, on_delete=models.SET_NULL, null=True, related_name="clases")
    tarifas = models.ManyToManyField(Tarifa, related_name="clases")
    capacidad = models.IntegerField(default=20)
    def __str__(self):
        return self.nombre

# ===========================
# USUARIOS CLIENTES
# ===========================
class Cliente(models.Model):

    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    password = models.CharField(max_length=255)
    tarifa = models.ForeignKey(Tarifa, on_delete=models.SET_NULL, null=True, related_name="usuarios")
    fecha_registro = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.nombre

# ===========================
# RESERVAS
# ===========================
class Reserva(models.Model):

    ESTADOS = [
        ('reservada', 'Reservada'),
        ('asistio', 'Asistió'),
        ('cancelada', 'Cancelada'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="reservas")
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name="reservas")
    fecha_reserva = models.DateField()
    estado = models.CharField(max_length=10, choices=ESTADOS, default='reservada')
    class Meta:
        unique_together = ('cliente', 'clase', 'fecha_reserva')

    def __str__(self):
        return f"{self.cliente} - {self.clase}"
