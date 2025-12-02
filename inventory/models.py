from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Cliente(models.Model):
    """
    Modelo para los clientes de fulfillment
    """
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Cliente")
    razon_social = models.CharField(max_length=200, verbose_name="Razón Social")
    rfc = models.CharField(max_length=13, unique=True, verbose_name="RFC")
    contacto = models.CharField(max_length=200, verbose_name="Persona de Contacto")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    email = models.EmailField(verbose_name="Correo Electrónico")
    direccion = models.TextField(verbose_name="Dirección")
    activo = models.BooleanField(default=True, verbose_name="Cliente Activo")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    notas = models.TextField(blank=True, null=True, verbose_name="Notas")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Ubicacion(models.Model):
    """
    Modelo para las ubicaciones dentro de la bodega
    """
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código de Ubicación")
    pasillo = models.CharField(max_length=10, verbose_name="Pasillo")
    estante = models.CharField(max_length=10, verbose_name="Estante")
    nivel = models.CharField(max_length=10, verbose_name="Nivel")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    capacidad_maxima = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Capacidad Máxima (m³)",
        null=True,
        blank=True
    )
    activo = models.BooleanField(default=True, verbose_name="Ubicación Activa")

    class Meta:
        verbose_name = "Ubicación"
        verbose_name_plural = "Ubicaciones"
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - Pasillo {self.pasillo}, Estante {self.estante}, Nivel {self.nivel}"


class Producto(models.Model):
    """
    Modelo para los productos de cada cliente
    """
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='productos',
        verbose_name="Cliente"
    )
    sku = models.CharField(max_length=100, verbose_name="SKU")
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    codigo_barras = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Código de Barras"
    )
    unidad_medida = models.CharField(
        max_length=50,
        default="PIEZA",
        verbose_name="Unidad de Medida"
    )
    peso = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Peso (kg)"
    )
    dimensiones = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Dimensiones (LxWxH cm)"
    )
    stock_minimo = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Stock Mínimo"
    )
    stock_maximo = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Stock Máximo"
    )
    imagen = models.ImageField(
        upload_to='productos/',
        blank=True,
        null=True,
        verbose_name="Imagen del Producto"
    )
    activo = models.BooleanField(default=True, verbose_name="Producto Activo")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['cliente', 'sku']
        unique_together = ['cliente', 'sku']

    def __str__(self):
        return f"{self.cliente.nombre} - {self.sku} - {self.nombre}"

    def stock_actual(self):
        """Retorna el stock actual total del producto"""
        total = self.inventarios.aggregate(
            total=models.Sum('cantidad')
        )['total']
        return total if total else 0


class Inventario(models.Model):
    """
    Modelo para el inventario actual en ubicaciones
    """
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='inventarios',
        verbose_name="Producto"
    )
    ubicacion = models.ForeignKey(
        Ubicacion,
        on_delete=models.CASCADE,
        related_name='inventarios',
        verbose_name="Ubicación"
    )
    cantidad = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Cantidad"
    )
    lote = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Número de Lote"
    )
    fecha_vencimiento = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha de Vencimiento"
    )
    ultima_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
        ordering = ['producto', 'ubicacion']
        unique_together = ['producto', 'ubicacion', 'lote']

    def __str__(self):
        return f"{self.producto.sku} - {self.ubicacion.codigo} - Cant: {self.cantidad}"


class TipoMovimiento(models.TextChoices):
    ENTRADA = 'ENTRADA', 'Entrada'
    SALIDA = 'SALIDA', 'Salida'
    AJUSTE_POSITIVO = 'AJUSTE_POS', 'Ajuste Positivo'
    AJUSTE_NEGATIVO = 'AJUSTE_NEG', 'Ajuste Negativo'
    TRANSFERENCIA = 'TRANSFERENCIA', 'Transferencia'


class Movimiento(models.Model):
    """
    Modelo para registrar todos los movimientos de inventario
    """
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='movimientos',
        verbose_name="Producto"
    )
    ubicacion = models.ForeignKey(
        Ubicacion,
        on_delete=models.CASCADE,
        related_name='movimientos',
        verbose_name="Ubicación"
    )
    tipo_movimiento = models.CharField(
        max_length=20,
        choices=TipoMovimiento.choices,
        verbose_name="Tipo de Movimiento"
    )
    cantidad = models.IntegerField(verbose_name="Cantidad")
    cantidad_anterior = models.IntegerField(verbose_name="Cantidad Anterior")
    cantidad_nueva = models.IntegerField(verbose_name="Cantidad Nueva")
    lote = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Número de Lote"
    )
    documento_referencia = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Documento de Referencia"
    )
    usuario = models.CharField(
        max_length=100,
        verbose_name="Usuario"
    )
    motivo = models.TextField(blank=True, null=True, verbose_name="Motivo/Observaciones")
    fecha_movimiento = models.DateTimeField(default=timezone.now, verbose_name="Fecha del Movimiento")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        verbose_name = "Movimiento"
        verbose_name_plural = "Movimientos"
        ordering = ['-fecha_movimiento']

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.producto.sku} - {self.cantidad} unidades - {self.fecha_movimiento.strftime('%d/%m/%Y %H:%M')}"
