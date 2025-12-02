from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('clientes/', views.clientes_list, name='clientes_list'),
    path('clientes/<int:cliente_id>/', views.cliente_detalle, name='cliente_detalle'),
    path('productos/', views.productos_list, name='productos_list'),
    path('productos/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),
    path('inventario/', views.inventario_general, name='inventario_general'),
    path('movimientos/', views.movimientos_list, name='movimientos_list'),
]
