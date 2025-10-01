from django.db import models
from django.contrib.auth.models import User  # ← Importa User

# Create your models here.

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class OrdenCompra(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ordenes_compra')  # ← Esta línea es nueva
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='ordenes')
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OC #{self.id} - {self.cliente.username} - {self.proveedor.nombre}"  # ← También actualiza esto

class DetalleOC(models.Model):
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.producto} x {self.cantidad} (OC #{self.orden.id})"
