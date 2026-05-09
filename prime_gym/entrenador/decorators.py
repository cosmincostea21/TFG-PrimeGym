from django.shortcuts import redirect
from gimnasio.models import Entrenador


def admin_required(view_func):

    def wrapper(request, *args, **kwargs):
        entrenador = Entrenador.objects.first()
        if not entrenador or entrenador.rol != "admin":
            return redirect('entrenador:panel')

        return view_func(request, *args, **kwargs)

    return wrapper