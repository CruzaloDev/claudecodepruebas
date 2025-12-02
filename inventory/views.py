from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Count, Q, F
from .models import Cliente, Producto, Inventario, Movimiento, Ubicacion


def dashboard(request):
    """
    Vista principal del dashboard con métricas generales
    """
    total_clientes = Cliente.objects.filter(activo=True).count()
    total_productos = Producto.objects.filter(activo=True).count()
    total_ubicaciones = Ubicacion.objects.filter(activo=True).count()

    # Stock total
    stock_total = Inventario.objects.aggregate(
        total=Sum('cantidad')
    )['total'] or 0

    # Productos con stock bajo
    productos_stock_bajo = Producto.objects.filter(
        activo=True
    ).annotate(
        stock_actual=Sum('inventarios__cantidad')
    ).filter(
        stock_actual__lt=F('stock_minimo')
    ).count()

    # Últimos movimientos
    ultimos_movimientos = Movimiento.objects.select_related(
        'producto', 'ubicacion', 'producto__cliente'
    ).order_by('-fecha_movimiento')[:10]

    # Clientes activos
    clientes = Cliente.objects.filter(activo=True).annotate(
        total_productos=Count('productos')
    ).order_by('nombre')

    context = {
        'total_clientes': total_clientes,
        'total_productos': total_productos,
        'total_ubicaciones': total_ubicaciones,
        'stock_total': stock_total,
        'productos_stock_bajo': productos_stock_bajo,
        'ultimos_movimientos': ultimos_movimientos,
        'clientes': clientes,
    }

    return render(request, 'inventory/dashboard.html', context)


def clientes_list(request):
    """
    Lista de todos los clientes
    """
    clientes = Cliente.objects.filter(activo=True).annotate(
        total_productos=Count('productos'),
        stock_total=Sum('productos__inventarios__cantidad')
    ).order_by('nombre')

    context = {
        'clientes': clientes,
    }

    return render(request, 'inventory/clientes_list.html', context)


def cliente_detalle(request, cliente_id):
    """
    Detalle de un cliente específico con sus productos e inventario
    """
    cliente = get_object_or_404(Cliente, id=cliente_id)

    productos = Producto.objects.filter(
        cliente=cliente,
        activo=True
    ).annotate(
        stock_actual=Sum('inventarios__cantidad')
    ).order_by('sku')

    movimientos_recientes = Movimiento.objects.filter(
        producto__cliente=cliente
    ).select_related(
        'producto', 'ubicacion'
    ).order_by('-fecha_movimiento')[:20]

    context = {
        'cliente': cliente,
        'productos': productos,
        'movimientos_recientes': movimientos_recientes,
    }

    return render(request, 'inventory/cliente_detalle.html', context)


def productos_list(request):
    """
    Lista de todos los productos
    """
    cliente_id = request.GET.get('cliente')

    productos = Producto.objects.filter(activo=True).select_related(
        'cliente'
    ).annotate(
        stock_actual=Sum('inventarios__cantidad')
    )

    if cliente_id:
        productos = productos.filter(cliente_id=cliente_id)

    productos = productos.order_by('cliente__nombre', 'sku')

    clientes = Cliente.objects.filter(activo=True).order_by('nombre')

    context = {
        'productos': productos,
        'clientes': clientes,
        'cliente_seleccionado': cliente_id,
    }

    return render(request, 'inventory/productos_list.html', context)


def producto_detalle(request, producto_id):
    """
    Detalle de un producto con su inventario por ubicación
    """
    producto = get_object_or_404(Producto, id=producto_id)

    inventarios = Inventario.objects.filter(
        producto=producto
    ).select_related('ubicacion').order_by('ubicacion__codigo')

    movimientos = Movimiento.objects.filter(
        producto=producto
    ).select_related('ubicacion').order_by('-fecha_movimiento')[:30]

    stock_total = inventarios.aggregate(total=Sum('cantidad'))['total'] or 0

    context = {
        'producto': producto,
        'inventarios': inventarios,
        'movimientos': movimientos,
        'stock_total': stock_total,
    }

    return render(request, 'inventory/producto_detalle.html', context)


def inventario_general(request):
    """
    Vista general del inventario por ubicaciones
    """
    ubicaciones = Ubicacion.objects.filter(activo=True).prefetch_related(
        'inventarios__producto__cliente'
    ).order_by('codigo')

    context = {
        'ubicaciones': ubicaciones,
    }

    return render(request, 'inventory/inventario_general.html', context)


def movimientos_list(request):
    """
    Lista de movimientos de inventario
    """
    tipo = request.GET.get('tipo')
    cliente_id = request.GET.get('cliente')

    movimientos = Movimiento.objects.select_related(
        'producto', 'ubicacion', 'producto__cliente'
    ).order_by('-fecha_movimiento')

    if tipo:
        movimientos = movimientos.filter(tipo_movimiento=tipo)

    if cliente_id:
        movimientos = movimientos.filter(producto__cliente_id=cliente_id)

    movimientos = movimientos[:100]  # Limitar a 100 registros

    clientes = Cliente.objects.filter(activo=True).order_by('nombre')

    context = {
        'movimientos': movimientos,
        'clientes': clientes,
        'tipo_seleccionado': tipo,
        'cliente_seleccionado': cliente_id,
    }

    return render(request, 'inventory/movimientos_list.html', context)
