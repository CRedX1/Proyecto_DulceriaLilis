from django.contrib import admin
from .models import Proveedor, OrdenCompra, DetalleOC

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'telefono', 'direccion']
    search_fields = ['nombre', 'telefono']
    list_filter = ['nombre']
    ordering = ['nombre']

class DetalleOCInline(admin.TabularInline):
    model = DetalleOC
    extra = 1
    fields = ['producto', 'cantidad', 'precio_unitario']

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'proveedor', 'fecha', 'total']
    list_filter = ['proveedor', 'fecha', 'cliente']
    search_fields = ['cliente__username', 'proveedor__nombre']
    date_hierarchy = 'fecha'
    inlines = [DetalleOCInline]
    ordering = ['-fecha']

@admin.register(DetalleOC)
class DetalleOCAdmin(admin.ModelAdmin):
    list_display = ['orden', 'producto', 'cantidad', 'precio_unitario']
    list_filter = ['producto']
    search_fields = ['producto', 'orden__id']
