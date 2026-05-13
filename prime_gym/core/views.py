from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroForm
from gimnasio.models import Cliente

def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # ✅ Guardar email
            user.email = form.cleaned_data['email']
            user.save()

            # ✅ Crear Cliente EXACTAMENTE como tú quieres
            Cliente.objects.create(
                user=user,
                telefono=form.cleaned_data['telefono'],
                tarifa=None
            )

            messages.success(
                request,
                "Cuenta creada correctamente. Ya puedes iniciar sesión."
            )
            return redirect('login')
        else:
            messages.error(request, "Revisa los datos del formulario.")
    else:
        form = RegistroForm()

    return render(request, 'registration/register.html', {'form': form})