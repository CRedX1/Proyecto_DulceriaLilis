from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Rol(models.Model):
    """
    Modelo para definir los roles de usuario en el sistema
    Ejemplo: Cliente, Administrador, Supervisor
    """
    # Constantes para los tipos de roles disponibles
    CLIENTE = 'cliente'
    ADMIN = 'admin'
    SUPERVISOR = 'supervisor'
    
    # Lista de opciones para el campo choices del modelo
    ROLES_CHOICES = [
        (CLIENTE, 'Cliente'),           # Valor en BD, Texto mostrado al usuario
        (ADMIN, 'Administrador'),
        (SUPERVISOR, 'Supervisor'),
    ]
    
    # Campo para almacenar el nombre del rol, debe ser único
    nombre = models.CharField(max_length=20, choices=ROLES_CHOICES, unique=True)

    def __str__(self):
        """Método que define cómo se muestra el objeto en el admin y consultas"""
        return self.get_nombre_display()  # Muestra el texto legible, no el valor de BD

class PerfilUsuario(models.Model):
    """
    Extensión del modelo User de Django para agregar campos específicos del negocio
    Cada User tiene un PerfilUsuario asociado (relación 1:1)
    """
    # Opciones de estado del usuario según requerimientos del negocio
    ESTADOS_CHOICES = [
        ('ACTIVO', 'Activo'),           # Usuario puede usar el sistema
        ('BLOQUEADO', 'Bloqueado'),     # Usuario temporalmente bloqueado
        ('DESACTIVADO', 'Desactivado'), # Usuario dado de baja
    ]
    
    # === RELACIONES ===
    # Relación uno a uno con el modelo User de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Si se elimina el User, se elimina automáticamente el PerfilUsuario
    
    # Relación con el modelo Rol (muchos usuarios pueden tener el mismo rol)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)
    # Si se elimina el Rol, el campo se pone en NULL, no se elimina el usuario
    
    # === CAMPOS DE CONTACTO ===
    telefono = models.CharField(max_length=30, blank=True)  # Opcional, puede estar vacío
    direccion = models.CharField(max_length=200, blank=True)  # Opcional
    
    # === CAMPOS DE CONTROL ===
    estado = models.CharField(max_length=12, choices=ESTADOS_CHOICES, default='ACTIVO')
    # Por defecto todos los usuarios están activos
    
    mfa_habilitado = models.BooleanField(default=False)  # Autenticación de doble factor
    ultimo_acceso = models.DateTimeField(null=True, blank=True)  # Se actualiza automáticamente
    
    # === CAMPOS ORGANIZACIONALES ===
    area_unidad = models.CharField(max_length=100, blank=True)  # Departamento del usuario
    observaciones = models.TextField(blank=True)  # Notas adicionales

    def __str__(self):
        """Representación del objeto como string"""
        return f"{self.user.username} - {self.rol}"

    # === MÉTODOS DE VERIFICACIÓN DE ROL ===
    def es_cliente(self):
        """Verifica si el usuario tiene rol de cliente"""
        return self.rol and self.rol.nombre == Rol.CLIENTE

    def es_admin(self):
        """Verifica si el usuario tiene rol de administrador"""
        return self.rol and self.rol.nombre == Rol.ADMIN
    
    def es_supervisor(self):
        """Verifica si el usuario tiene rol de supervisor"""
        return self.rol and self.rol.nombre == Rol.SUPERVISOR
    
    def esta_activo(self):
        """Verifica si el usuario está en estado activo"""
        return self.estado == 'ACTIVO'

# === SEÑALES (SIGNALS) ===
# Se ejecutan automáticamente cuando ocurren ciertos eventos

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """
    Señal que se ejecuta después de guardar un User
    Si el User es nuevo (created=True), crea automáticamente su PerfilUsuario
    """
    if created:  # Solo si es un usuario nuevo
        # Obtiene o crea el rol de cliente (rol por defecto)
        rol_cliente, _ = Rol.objects.get_or_create(nombre=Rol.CLIENTE)
        # Crea el perfil asociado al nuevo usuario
        PerfilUsuario.objects.create(user=instance, rol=rol_cliente)

@receiver(post_save, sender=User, dispatch_uid="update_last_login")
def actualizar_ultimo_acceso(sender, instance, **kwargs):
    """
    Señal para actualizar la fecha de último acceso
    Se ejecuta cada vez que se guarda un User
    """
    if hasattr(instance, 'perfilusuario'):  # Verifica que tenga perfil
        from django.utils import timezone
        instance.perfilusuario.ultimo_acceso = timezone.now()  # Fecha actual
        instance.perfilusuario.save()  # Guarda el cambio
