from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from gimnasio.models import Cliente

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username","first_name","last_name", "email", "password1", "password2")

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # eliminar textos informativos de password
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None

        
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True



    # Validar email único
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email



    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            Cliente.objects.create(
                user=user,
                tarifa=None  # mantenemos tu requisito
            )

        return user
