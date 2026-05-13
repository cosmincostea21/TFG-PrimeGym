from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from gimnasio.models import Cliente

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    telefono = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "telefono", "password1", "password2")

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # eliminar textos informativos de password
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None


    # Validar email único
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email

    # Validar teléfono
    def clean_telefono(self):
        telefono = self.cleaned_data.get("telefono")

        # quitar espacios
        telefono = telefono.strip()

        # Solo números (puedes permitir +34 si quieres, te lo explico abajo)
        if not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener solo números.")

        # longitud mínima/máxima
        if len(telefono) < 9:
            raise forms.ValidationError("El teléfono es demasiado corto.")

        if len(telefono) > 15:
            raise forms.ValidationError("El teléfono es demasiado largo.")

        return telefono

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            Cliente.objects.create(
                user=user,
                telefono=self.cleaned_data["telefono"],
                tarifa=None  # mantenemos tu requisito
            )

        return user
