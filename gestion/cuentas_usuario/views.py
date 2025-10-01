from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from proveedores.models import OrdenCompra
from proveedores.forms import OrdenCompraForm, DetalleOCForm

def inicio(request):
    return render(request, 'cuentas_usuario/inicio.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirigir según el rol
                if hasattr(user, 'perfilusuario') and user.perfilusuario.es_admin():
                    return redirect('cuentas_usuario:dashboard_admin')
                else:
                    return redirect('cuentas_usuario:dashboard_cliente')
    else:
        form = AuthenticationForm()
    return render(request, 'cuentas_usuario/login.html', {'form': form})

def registro_cliente(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Cuenta creada exitosamente. Puedes iniciar sesión.')
            return redirect('cuentas_usuario:login')
    else:
        form = UserCreationForm()
    return render(request, 'cuentas_usuario/registro.html', {'form': form})

@login_required
def dashboard_cliente(request):
    if hasattr(request.user, 'perfilusuario') and request.user.perfilusuario.es_admin():
        return redirect('cuentas_usuario:dashboard_admin')
    
    ordenes = OrdenCompra.objects.filter(cliente=request.user)
    return render(request, 'cuentas_usuario/dashboard_cliente.html', {
        'ordenes': ordenes,
        'user': request.user
    })

@login_required
def dashboard_admin(request):
    if not (hasattr(request.user, 'perfilusuario') and request.user.perfilusuario.es_admin()):
        return redirect('cuentas_usuario:dashboard_cliente')
    
    ordenes = OrdenCompra.objects.all()
    return render(request, 'cuentas_usuario/dashboard_admin.html', {
        'ordenes': ordenes,
        'user': request.user
    })

@login_required
def crear_orden_cliente(request):
    if hasattr(request.user, 'perfilusuario') and request.user.perfilusuario.es_admin():
        return redirect('cuentas_usuario:dashboard_admin')
    
    if request.method == 'POST':
        orden_form = OrdenCompraForm(request.POST)
        detalle_form = DetalleOCForm(request.POST)
        if orden_form.is_valid() and detalle_form.is_valid():
            orden = orden_form.save(commit=False)
            orden.cliente = request.user
            orden.save()
            detalle = detalle_form.save(commit=False)
            detalle.orden = orden
            detalle.save()
            messages.success(request, 'Orden creada exitosamente.')
            return redirect('cuentas_usuario:dashboard_cliente')
    else:
        orden_form = OrdenCompraForm()
        detalle_form = DetalleOCForm()
    
    return render(request, 'cuentas_usuario/crear_orden_cliente.html', {
        'orden_form': orden_form,
        'detalle_form': detalle_form
    })
