from django.contrib import admin
from django.utils.html import format_html
from .models import Cliente, Ubicacion, Producto, Inventario, Movimiento


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'rfc', 'contacto', 'telefono', 'email', 'activo', 'fecha_registro']
    list_filter = ['activo', 'fecha_registro']
    search_fields = ['nombre', 'razon_social', 'rfc', 'contacto', 'email']
    readonly_fields = ['fecha_registro']
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'razon_social', 'rfc', 'activo')
        }),
        ('Contacto', {
            'fields': ('contacto', 'telefono', 'email', 'direccion')
        }),
        ('Información Adicional', {
            'fields': ('notas', 'fecha_registro'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'pasillo', 'estante', 'nivel', 'capacidad_maxima', 'activo']
    list_filter = ['activo', 'pasillo']
    search_fields = ['codigo', 'pasillo', 'estante', 'nivel']
    fieldsets = (
        ('Ubicación', {
            'fields': ('codigo', 'pasillo', 'estante', 'nivel', 'activo')
        }),
        ('Detalles', {
            'fields': ('descripcion', 'capacidad_maxima')
        }),
    )


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['sku', 'nombre', 'cliente', 'unidad_medida', 'stock_actual_display', 'stock_minimo', 'activo', 'imagen_preview']
    list_filter = ['cliente', 'activo', 'fecha_registro']
    search_fields = ['sku', 'nombre', 'codigo_barras', 'cliente__nombre']
    readonly_fields = ['fecha_registro', 'imagen_preview']
    autocomplete_fields = ['cliente']

    fieldsets = (
        ('Información del Cliente', {
            'fields': ('cliente',)
        }),
        ('Información del Producto', {
            'fields': ('sku', 'nombre', 'descripcion', 'codigo_barras', 'unidad_medida', 'activo')
        }),
        ('Características Físicas', {
            'fields': ('peso', 'dimensiones', 'imagen', 'imagen_preview'),
            'classes': ('collapse',)
        }),
        ('Control de Stock', {
            'fields': ('stock_minimo', 'stock_maximo')
        }),
        ('Información del Sistema', {
            'fields': ('fecha_registro',),
            'classes': ('collapse',)
        }),
    )

    def stock_actual_display(self, obj):
        stock = obj.stock_actual()
        if stock < obj.stock_minimo:
            color = 'red'
        elif stock > obj.stock_maximo:
            color = 'orange'
        else:
            color = 'green'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            stock
        )
    stock_actual_display.short_description = 'Stock Actual'

    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 200px;" />',
                obj.imagen.url
            )
        return "Sin imagen"
    imagen_preview.short_description = 'Vista Previa'


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ['producto', 'ubicacion', 'cantidad', 'lote', 'fecha_vencimiento', 'ultima_actualizacion']
    list_filter = ['ubicacion', 'producto__cliente', 'fecha_vencimiento']
    search_fields = ['producto__sku', 'producto__nombre', 'ubicacion__codigo', 'lote']
    readonly_fields = ['ultima_actualizacion']
    autocomplete_fields = ['producto', 'ubicacion']

    fieldsets = (
        ('Producto y Ubicación', {
            'fields': ('producto', 'ubicacion')
        }),
        ('Cantidad', {
            'fields': ('cantidad',)
        }),
        ('Información del Lote', {
            'fields': ('lote', 'fecha_vencimiento'),
            'classes': ('collapse',)
        }),
        ('Sistema', {
            'fields': ('ultima_actualizacion',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ['fecha_movimiento', 'tipo_movimiento', 'producto', 'ubicacion', 'cantidad', 'usuario', 'documento_referencia']
    list_filter = ['tipo_movimiento', 'fecha_movimiento', 'producto__cliente']
    search_fields = ['producto__sku', 'producto__nombre', 'ubicacion__codigo', 'documento_referencia', 'usuario']
    readonly_fields = ['fecha_registro']
    autocomplete_fields = ['producto', 'ubicacion']
    date_hierarchy = 'fecha_movimiento'

    fieldsets = (
        ('Información del Movimiento', {
            'fields': ('tipo_movimiento', 'producto', 'ubicacion', 'fecha_movimiento')
        }),
        ('Cantidades', {
            'fields': ('cantidad', 'cantidad_anterior', 'cantidad_nueva')
        }),
        ('Detalles', {
            'fields': ('lote', 'documento_referencia', 'usuario', 'motivo')
        }),
        ('Sistema', {
            'fields': ('fecha_registro',),
            'classes': ('collapse',)
        }),
    )

    def has_delete_permission(self, request, obj=None):
        # Prevenir eliminación de movimientos para mantener trazabilidad
        return False


# Personalización del sitio de administración
admin.site.site_header = "Sistema de Fulfillment - Administración"
admin.site.site_title = "Fulfillment Admin"
admin.site.index_title = "Bienvenido al Sistema de Gestión de Inventario"
