from django import forms
from django.contrib.auth.models import User
from gimnasio.models import Cliente

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email'] # Aquí puedes agregar 'first_name' o 'last_name'

class ClienteUpdateForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['telefono']