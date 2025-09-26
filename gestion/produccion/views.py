from django.shortcuts import render

# Create your views here.
def inicio(request):
    contexto = {"nombre": "Dulcería Lilis"}
    return render(request, 'produccion/inicio.html', contexto)