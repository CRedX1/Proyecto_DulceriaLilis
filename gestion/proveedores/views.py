from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Proveedor, OrdenCompra, DetalleOC
from .forms import OrdenCompraForm, DetalleOCForm

# Create your views here.

def inicio(request):
    return HttpResponse("Bienvenido a la sección de Proveedores")

def lista_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedores/lista_proveedores.html', {'proveedores': proveedores})

def lista_ordenes(request):
    ordenes = OrdenCompra.objects.prefetch_related('detalles', 'proveedor').all()
    return render(request, 'proveedores/lista_ordenes.html', {'ordenes': ordenes})

def crear_orden(request):
    if request.method == 'POST':
        orden_form = OrdenCompraForm(request.POST)
        detalle_form = DetalleOCForm(request.POST)
        if orden_form.is_valid() and detalle_form.is_valid():
            orden = orden_form.save()
            detalle = detalle_form.save(commit=False)
            detalle.orden = orden
            detalle.save()
            return redirect('proveedores:ordenes')
    else:
        orden_form = OrdenCompraForm()
        detalle_form = DetalleOCForm()
    return render(request, 'proveedores/crear_orden.html', {
        'orden_form': orden_form,
        'detalle_form': detalle_form
    })

