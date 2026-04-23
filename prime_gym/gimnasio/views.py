from django.shortcuts import render

# Create your views here.

def main(request):
    return render(request,"gimnasio/index.html")

def clases(request):
    return render(request,"gimnasio/class-details.html")

def tarifas(request):
    return render(request,"gimnasio/services.html")

def equipo(request):
    return render(request,"gimnasio/team.html")

def contacto(request):
    return render(request,"gimnasio/contact.html")