from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from gimnasio.models import Cliente, Tarifa


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            # 1️⃣ Crear usuario correctamente
            user = form.save()

            # 3️⃣ Crear Cliente asociado sin tarifa 
            Cliente.objects.create(
                user=user,
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
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})