# Pryme Gym

Aplicación web desarrollada en **Django** para la gestión de un gimnasio, permitiendo la reserva de clases, administración de usuarios y un panel específico para entrenadores.

***

## Descripción

**Pryme Gym** es una plataforma que facilita la gestión de clases deportivas en un gimnasio. Permite a los usuarios registrarse, consultar clases disponibles y realizar reservas, mientras que los entrenadores pueden administrar sus grupos de alumnos de forma sencilla.

***

## Funcionalidades

### Usuarios

* Registro e inicio de sesión
* Gestión de perfil
* Visualización de clases disponibles
* Reserva de clases
* Cancelación de reservas

### Gestión de clases

* Listado de clases disponibles
* Control de capacidad por clase
* Visualización de horarios

### Panel de Entrenador

* Visualización de clases asignadas
* Gestión de miembros inscritos
* Control de asistencia (opcional si se implementa)
* Administración de cupos

### Administración

* Panel de administración de Django
* Gestión de usuarios, clases y reservas

***

## Tecnologías utilizadas

* **Backend**
  * Python
  * Django

* **Frontend**
  * HTML5
  * CSS3
  * JavaScript
  * Bootstrap

* **Base de datos**
  * SQLite (por defecto en desarrollo)

***

## Estructura del proyecto

```bash
pryme_gym/
│
├── manage.py
├── requirements.txt
├── pryme_gym/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── core/           # Gestión de usuarios
├── perfil/         # Clases y reservas
├── entrenadores/   # Panel de entrenador
│
└── templates/
    └── ...
```

***

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tuusuario/pryme-gym.git
cd pryme-gym
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

Activar entorno:

```bash
# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```


#### 2.1. Instalar dependencias

```bash
pip install -r requirements.txt
```


#### 2.2. Aplicar migraciones

```bash
python manage.py migrate
```

***

### 3. Crear superusuario

```bash
python manage.py createsuperuser
```


### 4. Ejecutar el servidor

```bash
python manage.py runserver
```

Accede a la app en:

```
http://127.0.0.1:8000/
```


### 5. Acceso al panel de administración

```
http://127.0.0.1:8000/admin/
```


## Ejemplo de flujo de uso

1. El usuario se registra
2. Accede a su perfil o directamente a reservas
3. Reserva una clase disponible    
***
1. El entrenador inicia sesión
2. Gestiona su grupo desde su panel
3. Realiza altas bajas o modificaciones de los miembros.


## Autores

**Pedro Ignacio Díaz Alejo**  
**Daniel Ávila Contento**  
**Marius Cosmin Costea**

