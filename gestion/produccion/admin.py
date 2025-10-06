from django.contrib import admin
from .models import Categoria, Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']
    ordering = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['sku', 'nombre', 'categoria', 'marca', 'precio_venta', 'stock_minimo', 'perishable']
    list_filter = ['categoria', 'marca', 'perishable', 'control_por_lote', 'control_por_serie']
    search_fields = ['sku', 'nombre', 'marca', 'modelo']
    ordering = ['sku']
    
    fieldsets = (
        ('Identificación', {
            'fields': ('sku', 'ean_upc', 'nombre', 'descripcion', 'categoria', 'marca', 'modelo')
        }),
        ('Unidades y Precios', {
            'fields': ('uom_compra', 'uom_venta', 'factor_conversion', 'costo_estandar', 'costo_promedio', 'precio_venta', 'impuesto_iva')
        }),
        ('Control de Stock', {
            'fields': ('stock_minimo', 'stock_maximo', 'punto_reorden', 'perishable', 'control_por_lote', 'control_por_serie')
        }),
        ('Archivos de Soporte', {
            'fields': ('imagen_url', 'ficha_tecnica_url'),
            'classes': ('collapse',)
        }),
    )
