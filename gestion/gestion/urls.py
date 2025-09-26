from django.contrib import admin
from django.urls import path

from produccion.views import inicio

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio) # Ruta para la vista de inicio de producción
]
