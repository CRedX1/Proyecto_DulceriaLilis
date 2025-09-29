from django.contrib import admin
from .models import Proveedor, OrdenCompra, DetalleOC

admin.site.register(Proveedor)
admin.site.register(OrdenCompra)
admin.site.register(DetalleOC)
