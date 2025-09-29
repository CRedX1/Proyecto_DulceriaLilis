from django.contrib import admin
from django.urls import path, include
from .view import inicio  # Importa la vista principal desde gestion/view.py

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio, name='inicio'),  # Página principal con menú
    path('produccion/', include('produccion.urls')),
    path('proveedores/', include('proveedores.urls')),
    path('ventas/', include('ventas.urls')),
    path('cuentas_usuario/', include('cuentas_usuario.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # <--- aquí va
]
