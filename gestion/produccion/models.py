from django.db import models

class Categoria(models.Model):
    """
    Modelo para clasificar productos en categorías
    Ejemplo: Chocolates, Dulces, Ingredientes, Postres, etc.
    """
    # Nombre único de la categoría (no puede haber duplicados)
    nombre = models.CharField(max_length=100, unique=True)
    # Descripción opcional de la categoría
    descripcion = models.TextField(blank=True)  # blank=True permite que esté vacío
    
    def __str__(self):
        """Representa la categoría como string (se muestra en select boxes del admin)"""
        return self.nombre
    
    class Meta:
        """Configuración adicional del modelo"""
        verbose_name = "Categoría"        # Nombre singular en el admin
        verbose_name_plural = "Categorías" # Nombre plural en el admin

class Producto(models.Model):
    """
    Modelo principal para productos de la dulcería
    Contiene toda la información comercial, de inventario y control
    """
    
    # === OPCIONES DE UNIDADES DE MEDIDA ===
    UOM_CHOICES = [
        ('UN', 'Unidad'),      # Para productos individuales (barras, piezas)
        ('CAJA', 'Caja'),      # Para empaque por cajas
        ('KG', 'Kilogramo'),   # Para productos por peso
        ('L', 'Litro'),        # Para líquidos
        ('DOCENA', 'Docena'),  # Para productos por docenas
        ('GRAMO', 'Gramo'),    # Para pequeñas cantidades
        ('PAQUETE', 'Paquete'), # Para empaques especiales
    ]
    
    # === SECCIÓN IDENTIFICACIÓN ===
    # Código único del producto (Stock Keeping Unit)
    sku = models.CharField(max_length=50, unique=True, verbose_name="SKU")
    
    # Código de barras internacional (opcional)
    ean_upc = models.CharField(
        max_length=20, 
        blank=True,     # Puede estar vacío
        unique=True,    # Si se usa, debe ser único
        null=True,      # Permite NULL en la base de datos
        verbose_name="EAN/UPC"
    )
    
    # Información básica del producto
    nombre = models.CharField(max_length=255)           # Nombre comercial
    descripcion = models.TextField(blank=True)          # Descripción detallada (opcional)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)  # Relación con Categoría
    # Si se elimina la categoría, se eliminan todos sus productos
    
    marca = models.CharField(max_length=100, blank=True)  # Marca del producto (opcional)
    modelo = models.CharField(max_length=100, blank=True) # Modelo específico (opcional)
    
    # === SECCIÓN UNIDADES Y PRECIOS ===
    # Unidad en que se compra el producto (ej: por cajas)
    uom_compra = models.CharField(max_length=10, choices=UOM_CHOICES, verbose_name="Unidad de Compra")
    
    # Unidad en que se vende el producto (ej: por unidades)
    uom_venta = models.CharField(max_length=10, choices=UOM_CHOICES, verbose_name="Unidad de Venta")
    
    # Factor de conversión entre unidad de compra y venta
    # Ej: Si compras por caja (12 unidades), factor = 12
    factor_conversion = models.DecimalField(
        max_digits=10, 
        decimal_places=4, 
        default=1, 
        verbose_name="Factor de Conversión"
    )
    
    # === PRECIOS ===
    # Costo estándar del producto (lo que debería costar)
    costo_estandar = models.DecimalField(
        max_digits=18,    # Hasta 18 dígitos en total
        decimal_places=6, # 6 decimales para precisión
        null=True,        # Puede ser NULL
        blank=True,       # Puede estar vacío en formularios
        verbose_name="Costo Estándar"
    )
    
    # Costo promedio ponderado (calculado automáticamente)
    costo_promedio = models.DecimalField(
        max_digits=18, 
        decimal_places=6, 
        null=True, 
        blank=True, 
        verbose_name="Costo Promedio"
    )
    
    # Precio de venta al público
    precio_venta = models.DecimalField(
        max_digits=18, 
        decimal_places=6, 
        null=True, 
        blank=True, 
        verbose_name="Precio de Venta"
    )
    
    # Porcentaje de IVA aplicable (por defecto 19% en Chile)
    impuesto_iva = models.DecimalField(
        max_digits=5,      # Máximo 99.99%
        decimal_places=2, 
        default=19.00, 
        verbose_name="IVA (%)"
    )
    
    # === SECCIÓN STOCK Y CONTROL ===
    # Stock mínimo antes de generar alerta de reposición
    stock_minimo = models.DecimalField(
        max_digits=18, 
        decimal_places=6, 
        default=0, 
        verbose_name="Stock Mínimo"
    )
    
    # Stock máximo recomendado (opcional)
    stock_maximo = models.DecimalField(
        max_digits=18, 
        decimal_places=6, 
        null=True, 
        blank=True, 
        verbose_name="Stock Máximo"
    )
    
    # Punto en el cual se debe generar orden de compra
    punto_reorden = models.DecimalField(
        max_digits=18, 
        decimal_places=6, 
        null=True, 
        blank=True, 
        verbose_name="Punto de Reorden"
    )
    
    # === CONTROLES ESPECIALES ===
    # Si el producto tiene fecha de vencimiento
    perishable = models.BooleanField(default=False, verbose_name="Es Perecedero")
    
    # Si se controla por lotes de producción
    control_por_lote = models.BooleanField(default=False, verbose_name="Control por Lote")
    
    # Si cada unidad tiene número de serie único
    control_por_serie = models.BooleanField(default=False, verbose_name="Control por Serie")
    
    # === ARCHIVOS DE SOPORTE ===
    # URL de imagen del producto (para catálogo web)
    imagen_url = models.URLField(blank=True, verbose_name="URL de Imagen")
    
    # URL de ficha técnica o especificaciones
    ficha_tecnica_url = models.URLField(blank=True, verbose_name="URL Ficha Técnica")
    
    # === METADATOS DE AUDITORÍA ===
    # Se llenan automáticamente
    fecha_creacion = models.DateTimeField(auto_now_add=True)    # Solo al crear
    fecha_modificacion = models.DateTimeField(auto_now=True)    # Cada vez que se modifica
    
    def __str__(self):
        """Representación del producto como string"""
        return f"{self.sku} - {self.nombre}"
    
    # === PROPIEDADES CALCULADAS ===
    @property
    def stock_actual(self):
        """
        Calcula el stock actual del producto
        TODO: Se implementará cuando se cree el módulo de inventario
        """
        return 0  # Placeholder - valor temporal
    
    @property
    def alerta_bajo_stock(self):
        """
        Verifica si el producto está bajo el stock mínimo
        Retorna True si necesita reposición
        """
        return self.stock_actual <= self.stock_minimo
    
    class Meta:
        """Configuración adicional del modelo"""
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['sku']  # Ordenar por SKU por defecto
