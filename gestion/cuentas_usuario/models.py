from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Rol(models.Model):
    CLIENTE = 'cliente'
    ADMIN = 'admin'
    
    ROLES_CHOICES = [
        (CLIENTE, 'Cliente'),
        (ADMIN, 'Administrador'),
    ]
    
    nombre = models.CharField(max_length=20, choices=ROLES_CHOICES, unique=True)

    def __str__(self):
        return self.get_nombre_display()

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"

    def es_cliente(self):
        return self.rol and self.rol.nombre == Rol.CLIENTE

    def es_admin(self):
        return self.rol and self.rol.nombre == Rol.ADMIN

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        # Por defecto, asignar rol de cliente
        rol_cliente, _ = Rol.objects.get_or_create(nombre=Rol.CLIENTE)
        PerfilUsuario.objects.create(user=instance, rol=rol_cliente)
