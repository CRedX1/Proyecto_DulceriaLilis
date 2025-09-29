from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

def inicio(request):
    return HttpResponse("Bienvenido a la sección de Cuentas de Usuario")

@login_required
def perfil(request):
    perfil = request.user.perfilusuario
    return render(request, 'cuentas_usuario/perfil.html', {'perfil': perfil})
