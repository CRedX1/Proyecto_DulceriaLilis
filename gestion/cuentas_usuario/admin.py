from django.contrib import admin
from .models import PerfilUsuario, Rol

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'rol', 'estado', 'telefono', 'mfa_habilitado', 'ultimo_acceso']
    list_filter = ['rol', 'estado', 'mfa_habilitado']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'telefono']
    ordering = ['user__username']
    readonly_fields = ['ultimo_acceso']  # Solo lectura para último acceso
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user', 'rol', 'estado')
        }),
        ('Contacto', {
            'fields': ('telefono', 'direccion')
        }),
        ('Seguridad', {
            'fields': ('mfa_habilitado', 'ultimo_acceso')
        }),
        ('Información Adicional', {
            'fields': ('area_unidad', 'observaciones'),
            'classes': ('collapse',)  # Sección colapsable
        }),
    )
