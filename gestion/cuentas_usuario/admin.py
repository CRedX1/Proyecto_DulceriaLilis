from django.contrib import admin
from .models import PerfilUsuario, Rol

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'rol', 'telefono', 'direccion']
    list_filter = ['rol']
    search_fields = ['user__username', 'user__email', 'telefono']
    ordering = ['user__username']
