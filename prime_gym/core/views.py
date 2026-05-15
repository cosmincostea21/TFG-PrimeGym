from django.shortcuts import render, redirect
from django.contrib import messages
from gimnasio.models import Cliente


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroForm

def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)

        if form.is_valid():
            form.save()  # ✅ usa tu lógica del form

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