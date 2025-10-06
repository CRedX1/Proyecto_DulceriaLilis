from django.db import models
from django.contrib.auth.models import User
from produccion.models import Producto
from decimal import Decimal

# =============================================================================
# MODELOS PARA LA GESTIÓN DE PROVEEDORES Y COMPRAS
# =============================================================================
# Este archivo contiene los modelos relacionados con la gestión de proveedores,
# sus productos, y el sistema de órdenes de compra de la dulcería.

class Proveedor(models.Model):
    """
    Modelo que representa a un proveedor de productos para la dulcería.
    
    Almacena tanto información básica de contacto como datos legales y 
    comerciales necesarios para las transacciones comerciales.
    """
    
    # === INFORMACIÓN BÁSICA ===
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre del Proveedor",
        help_text="Nombre comercial del proveedor"
    )
    
    razon_social = models.CharField(
        max_length=150,
        verbose_name="Razón Social",
        help_text="Razón social legal de la empresa proveedora",
        blank=True,
        null=True
    )
    
    rfc = models.CharField(
        max_length=13,
        verbose_name="RFC",
        help_text="Registro Federal de Contribuyentes del proveedor",
        unique=True,
        blank=True,
        null=True
    )
    
    # === INFORMACIÓN DE CONTACTO ===
    telefono = models.CharField(
        max_length=20,
        verbose_name="Teléfono",
        help_text="Número telefónico principal del proveedor"
    )
    
    email = models.EmailField(
        verbose_name="Correo Electrónico",
        help_text="Email de contacto del proveedor",
        blank=True,
        null=True
    )
    
    direccion = models.CharField(
        max_length=200,
        verbose_name="Dirección",
        help_text="Dirección física del proveedor"
    )
    
    ciudad = models.CharField(
        max_length=100,
        verbose_name="Ciudad",
        help_text="Ciudad donde se ubica el proveedor",
        blank=True,
        null=True
    )
    
    codigo_postal = models.CharField(
        max_length=10,
        verbose_name="Código Postal",
        help_text="Código postal de la dirección del proveedor",
        blank=True,
        null=True
    )
    
    # === INFORMACIÓN COMERCIAL ===
    dias_credito = models.PositiveIntegerField(
        verbose_name="Días de Crédito",
        help_text="Número de días de crédito que otorga el proveedor",
        default=0
    )
    
    descuento_pronto_pago = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Descuento Pronto Pago (%)",
        help_text="Porcentaje de descuento por pronto pago",
        default=0.00
    )
    
    limite_credito = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Límite de Crédito",
        help_text="Límite de crédito otorgado por el proveedor",
        default=0.00
    )
    
    # === CONTROL DE ESTADO ===
    activo = models.BooleanField(
        default=True,
        verbose_name="Proveedor Activo",
        help_text="Indica si el proveedor está activo para realizar compras"
    )
    
    # === FECHAS DE CONTROL ===
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro",
        help_text="Fecha y hora en que se registró el proveedor"
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Modificación",
        help_text="Fecha y hora de la última modificación"
    )
    
    # === NOTAS Y OBSERVACIONES ===
    notas = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notas",
        help_text="Notas adicionales sobre el proveedor"
    )
    
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.telefono}"


class ProductoProveedor(models.Model):
    """
    Modelo intermedio para la relación muchos a muchos entre Producto y Proveedor.
    
    Permite almacenar información específica de cada producto por proveedor,
    como códigos internos, precios especiales, y tiempos de entrega.
    """
    
    # === RELACIONES ===
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        verbose_name="Producto",
        help_text="Producto que suministra el proveedor"
    )
    
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE,
        verbose_name="Proveedor",
        help_text="Proveedor que suministra el producto"
    )
    
    # === INFORMACIÓN COMERCIAL ===
    codigo_proveedor = models.CharField(
        max_length=50,
        verbose_name="Código del Proveedor",
        help_text="Código interno que usa el proveedor para este producto",
        blank=True,
        null=True
    )
    
    precio_compra = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio de Compra",
        help_text="Precio de compra del producto a este proveedor"
    )
    
    precio_con_descuento = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio con Descuento",
        help_text="Precio con descuento aplicado (si aplica)",
        blank=True,
        null=True
    )
    
    # === LOGÍSTICA ===
    tiempo_entrega_dias = models.PositiveIntegerField(
        verbose_name="Tiempo de Entrega (días)",
        help_text="Días que tarda el proveedor en entregar este producto",
        default=1
    )
    
    cantidad_minima = models.PositiveIntegerField(
        verbose_name="Cantidad Mínima",
        help_text="Cantidad mínima de pedido para este producto",
        default=1
    )
    
    # === CONTROL ===
    es_proveedor_preferido = models.BooleanField(
        default=False,
        verbose_name="Proveedor Preferido",
        help_text="Indica si este es el proveedor preferido para este producto"
    )
    
    fecha_ultimo_precio = models.DateField(
        verbose_name="Fecha Último Precio",
        help_text="Fecha de la última actualización de precio",
        auto_now=True
    )
    
    class Meta:
        verbose_name = "Producto-Proveedor"
        verbose_name_plural = "Productos-Proveedores"
        unique_together = ['producto', 'proveedor']
        ordering = ['producto__nombre', 'proveedor__nombre']
    
    def __str__(self):
        return f"{self.producto.nombre} - {self.proveedor.nombre} (${self.precio_compra})"


class OrdenCompra(models.Model):
    """
    Modelo que representa una orden de compra realizada a un proveedor.
    
    Contiene la información general de la compra: quién la realizó,
    a qué proveedor, cuándo, y el total de la orden.
    """
    
    # === RELACIONES PRINCIPALES ===
    cliente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ordenes_compra',
        verbose_name="Usuario que Realiza la Compra",
        help_text="Usuario del sistema que está realizando esta orden de compra"
    )
    
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE,
        related_name='ordenes',
        verbose_name="Proveedor",
        help_text="Proveedor al que se le está comprando"
    )
    
    # === INFORMACIÓN DE LA ORDEN ===
    numero_orden = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Número de Orden",
        help_text="Número único de identificación de la orden de compra",
        blank=True,
        null=True
    )
    
    fecha = models.DateField(
        verbose_name="Fecha de la Orden",
        help_text="Fecha en que se realizó la orden de compra"
    )
    
    fecha_entrega_esperada = models.DateField(
        verbose_name="Fecha de Entrega Esperada",
        help_text="Fecha esperada para la entrega de los productos",
        blank=True,
        null=True
    )
    
    # === ESTADOS DE LA ORDEN ===
    ESTADOS_ORDEN = [
        ('pendiente', 'Pendiente'),
        ('enviada', 'Enviada al Proveedor'),
        ('confirmada', 'Confirmada por Proveedor'),
        ('parcial', 'Entrega Parcial'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_ORDEN,
        default='pendiente',
        verbose_name="Estado de la Orden",
        help_text="Estado actual de la orden de compra"
    )
    
    # === INFORMACIÓN FINANCIERA ===
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Subtotal",
        help_text="Subtotal de la orden (sin impuestos)",
        default=0.00
    )
    
    impuestos = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Impuestos",
        help_text="Total de impuestos aplicados",
        default=0.00
    )
    
    descuento = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Descuento",
        help_text="Descuento aplicado a la orden",
        default=0.00
    )
    
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Total de la Orden",
        help_text="Total final de la orden de compra"
    )
    
    # === OBSERVACIONES ===
    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observaciones",
        help_text="Observaciones adicionales sobre la orden de compra"
    )
    
    class Meta:
        verbose_name = "Orden de Compra"
        verbose_name_plural = "Órdenes de Compra"
        ordering = ['-fecha']
    
    def __str__(self):
        numero = self.numero_orden or f"#{self.id}"
        return f"OC {numero} - {self.cliente.username} - {self.proveedor.nombre}"
    
    def save(self, *args, **kwargs):
        """
        Calcula automáticamente los totales basándose en los detalles
        """
        # Primero guardar para tener ID
        super().save(*args, **kwargs)
        
        # Calcular subtotal de todos los detalles
        self.subtotal = sum(detalle.subtotal_linea for detalle in self.detalles.all())
        
        # Calcular impuestos (16%)
        base_gravable = self.subtotal - self.descuento
        self.impuestos = base_gravable * Decimal('0.16')
        
        # Calcular total
        self.total = base_gravable + self.impuestos
        
        # Guardar nuevamente con los cálculos
        super().save(*args, **kwargs)


class DetalleOC(models.Model):
    """
    Modelo que representa cada línea/producto dentro de una orden de compra.
    
    Cada DetalleOC representa un producto específico, su cantidad,
    precio unitario y cálculos relacionados dentro de la orden.
    """
    
    # === RELACIÓN CON LA ORDEN ===
    orden = models.ForeignKey(
        OrdenCompra,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name="Orden de Compra",
        help_text="Orden de compra a la que pertenece este detalle"
    )
    
    # === INFORMACIÓN DEL PRODUCTO ===
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        verbose_name="Producto",
        help_text="Producto que se está comprando"
    )
    
    # === CANTIDADES Y PRECIOS ===
    cantidad = models.PositiveIntegerField(
        verbose_name="Cantidad",
        help_text="Cantidad del producto a comprar"
    )
    
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio Unitario",
        help_text="Precio unitario del producto en esta compra"
    )
    
    descuento_linea = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Descuento por Línea",
        help_text="Descuento aplicado específicamente a esta línea",
        default=0.00
    )
    
    # === CAMPOS CALCULADOS ===
    subtotal_linea = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Subtotal de Línea",
        help_text="Subtotal de esta línea (cantidad × precio_unitario - descuento)",
        default=0.00
    )
    
    # === CONTROL DE ENTREGA ===
    cantidad_recibida = models.PositiveIntegerField(
        verbose_name="Cantidad Recibida",
        help_text="Cantidad realmente recibida del producto",
        default=0
    )
    
    fecha_recepcion = models.DateField(
        verbose_name="Fecha de Recepción",
        help_text="Fecha en que se recibió el producto",
        blank=True,
        null=True
    )
    
    # === NOTAS DEL DETALLE ===
    notas_detalle = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notas del Detalle",
        help_text="Notas específicas sobre este producto en la orden"
    )
    
    class Meta:
        verbose_name = "Detalle de Orden de Compra"
        verbose_name_plural = "Detalles de Órdenes de Compra"
        ordering = ['producto__nombre']
    
    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad} (OC #{self.orden.id})"
    
    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para calcular automáticamente el subtotal_linea
        cada vez que se guarda un detalle de orden de compra.
        """
        # Calcula el subtotal: (cantidad × precio_unitario) - descuento_linea
        self.subtotal_linea = (self.cantidad * self.precio_unitario) - self.descuento_linea
        super().save(*args, **kwargs)
