from django import forms
from gimnasio.models import Cliente

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'telefono']

class CambiarPasswordForm(forms.Form):
    password_actual = forms.CharField(
        widget=forms.PasswordInput,
        required=False
    )
    password_nueva = forms.CharField(
        widget=forms.PasswordInput,
        required=False
    )
    password_nueva_confirmacion = forms.CharField(
        widget=forms.PasswordInput,
        required=False
    )
