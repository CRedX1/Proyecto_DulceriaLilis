from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
from decimal import Decimal
import csv
from .models import Proveedor, ProductoProveedor, OrdenCompra, DetalleOC

# =============================================================================
# ACCIONES PERSONALIZADAS PARA DULCERÍA LILIS
# =============================================================================

# === ACCIONES PARA PROVEEDORES ===
@admin.action(description="Activar proveedores seleccionados")
def activar_proveedores(modeladmin, request, queryset):
    """Activa múltiples proveedores para poder realizar compras"""
    updated = queryset.update(activo=True)
    modeladmin.message_user(request, f'✅ {updated} proveedores activados correctamente.')

@admin.action(description="Desactivar proveedores seleccionados") 
def desactivar_proveedores(modeladmin, request, queryset):
    """Desactiva proveedores temporalmente"""
    updated = queryset.update(activo=False)
    modeladmin.message_user(request, f'❌ {updated} proveedores desactivados.')

@admin.action(description="Exportar proveedores a CSV")
def exportar_proveedores_csv(modeladmin, request, queryset):
    """Exporta información de proveedores seleccionados a archivo CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="proveedores_dulceria_lilis.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Nombre', 'RFC', 'Teléfono', 'Email', 'Ciudad', 'Días Crédito', 'Límite Crédito', 'Activo'])
    
    for proveedor in queryset:
        writer.writerow([
            proveedor.nombre,
            proveedor.rfc or 'N/A',
            proveedor.telefono,
            proveedor.email or 'N/A',
            proveedor.ciudad or 'N/A',
            proveedor.dias_credito,
            proveedor.limite_credito,
            'Sí' if proveedor.activo else 'No'
        ])
    
    return response

# === ACCIONES PARA ÓRDENES DE COMPRA ===
@admin.action(description="Marcar órdenes como Enviadas al Proveedor")
def enviar_ordenes_proveedor(modeladmin, request, queryset):
    """Cambia el estado de órdenes a 'Enviada al Proveedor'"""
    updated = queryset.update(estado='enviada')
    modeladmin.message_user(request, f'📤 {updated} órdenes marcadas como enviadas al proveedor.')

@admin.action(description="Marcar órdenes como Completadas")
def completar_ordenes(modeladmin, request, queryset):
    """Marca órdenes como completadas"""
    updated = queryset.update(estado='completada')
    modeladmin.message_user(request, f'✅ {updated} órdenes completadas exitosamente.')

@admin.action(description="Cancelar órdenes seleccionadas")
def cancelar_ordenes(modeladmin, request, queryset):
    """Cancela órdenes de compra"""
    updated = queryset.update(estado='cancelada')
    modeladmin.message_user(request, f'❌ {updated} órdenes canceladas.')

@admin.action(description="Exportar órdenes a CSV")
def exportar_ordenes_csv(modeladmin, request, queryset):
    """Exporta órdenes de compra a CSV con detalles completos"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ordenes_compra_dulceria.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Número Orden', 'Proveedor', 'Cliente', 'Fecha', 'Estado', 'Subtotal', 'Impuestos', 'Total'])
    
    for orden in queryset:
        writer.writerow([
            orden.numero_orden or f"#{orden.id}",
            orden.proveedor.nombre,
            orden.cliente.username,
            orden.fecha,
            dict(orden.ESTADOS_ORDEN)[orden.estado],
            orden.subtotal,
            orden.impuestos,
            orden.total
        ])
    
    return response

@admin.action(description="Generar números de orden automáticos")
def generar_numeros_orden(modeladmin, request, queryset):
    """Genera números de orden automáticos para órdenes sin número"""
    contador = 0
    año_actual = timezone.now().year
    
    for orden in queryset.filter(numero_orden__isnull=True):
        contador += 1
        orden.numero_orden = f"OC-{año_actual}-{orden.id:04d}"
        orden.save()
    
    modeladmin.message_user(request, f'🔢 Se generaron {contador} números de orden automáticos.')

# === ACCIONES PARA PRODUCTO-PROVEEDOR ===
@admin.action(description="Marcar como Proveedor Preferido")
def marcar_proveedor_preferido(modeladmin, request, queryset):
    """Marca relaciones como proveedor preferido"""
    updated = queryset.update(es_proveedor_preferido=True)
    modeladmin.message_user(request, f'⭐ {updated} proveedores marcados como preferidos.')

@admin.action(description="Quitar Proveedor Preferido")
def quitar_proveedor_preferido(modeladmin, request, queryset):
    """Quita la marca de proveedor preferido"""
    updated = queryset.update(es_proveedor_preferido=False)
    modeladmin.message_user(request, f'➖ {updated} proveedores ya no son preferidos.')

@admin.action(description="Aumentar precios 5%")
def aumentar_precios_5_porciento(modeladmin, request, queryset):
    """Aumenta precios de compra en 5%"""
    contador = 0
    for producto_proveedor in queryset:
        precio_anterior = producto_proveedor.precio_compra
        producto_proveedor.precio_compra = precio_anterior * Decimal('1.05')
        producto_proveedor.save()
        contador += 1
    
    modeladmin.message_user(request, f'💰 Precios aumentados 5% para {contador} productos.')

# ===================================================================
# INLINES - Configuraciones para mostrar modelos relacionados
# ===================================================================

class ProductoProveedorInline(admin.TabularInline):
    """
    Inline para mostrar los productos que surte un proveedor
    directamente en el formulario del proveedor.
    """
    model = ProductoProveedor
    extra = 1  # Una fila extra vacía para agregar nuevos productos
    fields = ['producto', 'codigo_proveedor', 'precio_compra', 'tiempo_entrega_dias', 'es_proveedor_preferido']
    
class DetalleOCInline(admin.TabularInline):
    """
    Inline para agregar productos a una orden de compra
    directamente en el formulario de la orden.
    """
    model = DetalleOC
    extra = 1  # Una fila extra vacía para agregar nuevos productos
    fields = ['producto', 'cantidad', 'precio_unitario', 'descuento_linea', 'cantidad_recibida']
    
class OrdenCompraInline(admin.TabularInline):
    """
    Inline para mostrar las órdenes de compra de un proveedor
    directamente en el formulario del proveedor.
    """
    model = OrdenCompra
    extra = 0  # No mostrar filas vacías (solo las existentes)
    fields = ['numero_orden', 'fecha', 'estado', 'total']
    readonly_fields = ['numero_orden', 'fecha', 'total']  # Solo lectura
    can_delete = False  # No permitir eliminar desde aquí
    show_change_link = True  # Mostrar enlace para editar la orden completa

# ===================================================================
# ADMIN CLASSES - Configuraciones de los modelos en el admin
# ===================================================================

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'telefono', 'email', 'ciudad', 'activo']
    search_fields = ['nombre', 'telefono', 'email', 'rfc']
    list_filter = ['activo', 'ciudad', 'dias_credito']
    ordering = ['nombre']
    
    # 🚀 ACCIONES PERSONALIZADAS PARA PROVEEDORES
    actions = [activar_proveedores, desactivar_proveedores, exportar_proveedores_csv]
    
    # Agregamos los inlines para ver productos y órdenes del proveedor
    inlines = [ProductoProveedorInline, OrdenCompraInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'razon_social', 'rfc')
        }),
        ('Contacto', {
            'fields': ('telefono', 'email', 'direccion', 'ciudad', 'codigo_postal')
        }),
        ('Información Comercial', {
            'fields': ('dias_credito', 'descuento_pronto_pago', 'limite_credito', 'activo')
        }),
        ('Observaciones', {
            'fields': ('notas',),
            'classes': ('collapse',)
        })
    )

@admin.register(ProductoProveedor)
class ProductoProveedorAdmin(admin.ModelAdmin):
    list_display = ['producto', 'proveedor', 'precio_compra', 'tiempo_entrega_dias', 'es_proveedor_preferido']
    list_filter = ['es_proveedor_preferido', 'tiempo_entrega_dias', 'proveedor']
    search_fields = ['producto__nombre', 'proveedor__nombre', 'codigo_proveedor']
    ordering = ['producto__nombre', 'proveedor__nombre']
    
    # 🚀 ACCIONES PERSONALIZADAS PARA PRODUCTO-PROVEEDOR
    actions = [marcar_proveedor_preferido, quitar_proveedor_preferido, aumentar_precios_5_porciento]
    
    # Fieldsets para organizar mejor la información
    fieldsets = (
        ('Relación Principal', {
            'fields': ('producto', 'proveedor')
        }),
        ('Información Comercial', {
            'fields': ('codigo_proveedor', 'precio_compra', 'precio_con_descuento')
        }),
        ('Logística', {
            'fields': ('tiempo_entrega_dias', 'cantidad_minima', 'es_proveedor_preferido')
        })
    )

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ['numero_orden', 'cliente', 'proveedor', 'fecha', 'estado', 'total']
    list_filter = ['estado', 'proveedor', 'fecha', 'cliente']
    search_fields = ['cliente__username', 'proveedor__nombre', 'numero_orden']
    date_hierarchy = 'fecha'
    inlines = [DetalleOCInline]  # Inline para agregar productos a la orden
    ordering = ['-fecha']
    
    # 🚀 ACCIONES PERSONALIZADAS PARA ÓRDENES
    actions = [enviar_ordenes_proveedor, completar_ordenes, cancelar_ordenes, 
              exportar_ordenes_csv, generar_numeros_orden]
    
    fieldsets = (
        ('Información de la Orden', {
            'fields': ('numero_orden', 'cliente', 'proveedor', 'fecha', 'fecha_entrega_esperada', 'estado')
        }),
        ('Totales', {
            'fields': ('subtotal', 'descuento', 'impuestos', 'total')
        }),
        ('Observaciones', {
            'fields': ('observaciones',),
            'classes': ('collapse',)
        })
    )
    
    class Media:
        js = ('admin/js/calcular_totales.js',)

@admin.register(DetalleOC)
class DetalleOCAdmin(admin.ModelAdmin):
    list_display = ['orden', 'producto', 'cantidad', 'precio_unitario', 'subtotal_linea', 'cantidad_recibida']
    list_filter = ['producto', 'orden__estado']
    search_fields = ['producto__nombre', 'orden__numero_orden']
    
    fieldsets = (
        ('Información del Producto', {
            'fields': ('orden', 'producto')
        }),
        ('Cantidades y Precios', {
            'fields': ('cantidad', 'precio_unitario', 'descuento_linea', 'subtotal_linea')
        }),
        ('Control de Entrega', {
            'fields': ('cantidad_recibida', 'fecha_recepcion')
        }),
        ('Observaciones', {
            'fields': ('notas_detalle',),
            'classes': ('collapse',)
        })
    )
    
    # El subtotal_linea se calcula automáticamente
    readonly_fields = ['subtotal_linea']
