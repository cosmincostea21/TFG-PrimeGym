from django import forms
from django.contrib.auth.models import User
from gimnasio.models import Cliente
import re
from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from gimnasio.models import Cliente


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")

        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Introduce un correo electrónico válido.")
        return email



class ClienteUpdateForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['telefono']

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')

        # Ejemplo: solo números, entre 9 y 15 dígitos
        if not re.match(r'^\d{9}$', telefono):
            raise forms.ValidationError(
                "El teléfono debe contener solo números y tener 9 dígitos."
            )

        return telefono
