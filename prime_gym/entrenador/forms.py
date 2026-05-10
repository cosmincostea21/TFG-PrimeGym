from django import forms
from django.contrib.auth.models import User
from gimnasio.models import Entrenador

class CrearEntrenadorForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    ROL_CHOICES = (
        ('empleado', 'Empleado'),
        ('admin', 'Admin'),
    )

    rol = forms.ChoiceField(choices=ROL_CHOICES)
    telefono = forms.CharField(required=False)
    especialidad = forms.CharField(required=False)