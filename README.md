# Sistema de Fulfillment - Gestión de Inventario

Sistema completo de gestión de inventario para empresas de fulfillment desarrollado en Django.

## Características

- **Gestión de Clientes**: Administra múltiples clientes de fulfillment
- **Control de Productos**: Catálogo completo de productos por cliente
- **Gestión de Ubicaciones**: Organización de bodega por pasillos, estantes y niveles
- **Control de Inventario**: Seguimiento de stock en tiempo real por ubicación
- **Historial de Movimientos**: Registro completo de entradas, salidas y ajustes
- **Alertas de Stock**: Notificaciones de stock bajo/alto
- **Panel de Administración**: Interface completa de Django Admin
- **Dashboard Web**: Interface web intuitiva con métricas en tiempo real

## Modelos de Datos

### Cliente
- Información de contacto y facturación
- RFC y razón social
- Estado activo/inactivo

### Producto
- SKU único por cliente
- Códigos de barras
- Especificaciones físicas (peso, dimensiones)
- Niveles de stock mínimo/máximo
- Imágenes de producto

### Ubicación
- Código de ubicación único
- Organización por pasillo/estante/nivel
- Capacidad máxima

### Inventario
- Stock por producto y ubicación
- Control de lotes
- Fechas de vencimiento

### Movimiento
- Tipos: Entrada, Salida, Ajuste Positivo, Ajuste Negativo, Transferencia
- Trazabilidad completa
- Usuario responsable
- Documento de referencia

## Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd claudecodepruebas
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate  # En Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear superusuario

```bash
python manage.py createsuperuser
```

### 6. Ejecutar el servidor

```bash
python manage.py runserver
```

El sistema estará disponible en: `http://127.0.0.1:8000/`

## Uso

### Panel de Administración

Accede a `http://127.0.0.1:8000/admin/` con las credenciales del superusuario para:

- Agregar clientes
- Registrar productos
- Crear ubicaciones en bodega
- Gestionar inventario
- Registrar movimientos

### Interface Web

Accede a `http://127.0.0.1:8000/` para:

- **Dashboard**: Vista general con métricas y últimos movimientos
- **Clientes**: Lista de clientes y sus productos
- **Productos**: Catálogo completo de productos con filtros
- **Inventario**: Vista de inventario por ubicaciones
- **Movimientos**: Historial completo de movimientos

## Flujo de Trabajo Recomendado

1. **Configuración Inicial**:
   - Crear ubicaciones en bodega (Admin → Ubicaciones)
   - Registrar clientes (Admin → Clientes)
   - Agregar productos por cliente (Admin → Productos)

2. **Operación Diaria**:
   - Registrar entradas de mercancía (Admin → Movimientos → Agregar)
   - Registrar salidas de producto
   - Realizar ajustes de inventario cuando sea necesario
   - Consultar stock en tiempo real desde el Dashboard

3. **Monitoreo**:
   - Revisar productos con stock bajo desde el Dashboard
   - Verificar movimientos por cliente
   - Auditar historial de movimientos

## Estructura del Proyecto

```
claudecodepruebas/
├── fulfillment/          # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── inventory/            # Aplicación de inventario
│   ├── models.py        # Modelos de datos
│   ├── views.py         # Vistas
│   ├── admin.py         # Configuración del admin
│   ├── urls.py          # URLs
│   └── templates/       # Templates HTML
├── manage.py
└── requirements.txt
```

## Configuración de Producción

Para usar en producción:

1. Cambiar `DEBUG = False` en `settings.py`
2. Configurar `ALLOWED_HOSTS` con tu dominio
3. Cambiar `SECRET_KEY` por una clave segura
4. Configurar base de datos PostgreSQL o MySQL
5. Configurar archivos estáticos con `collectstatic`
6. Usar servidor WSGI como Gunicorn
7. Configurar servidor web (Nginx/Apache)

## Tecnologías Utilizadas

- **Django 4.2.7**: Framework web
- **Python 3.x**: Lenguaje de programación
- **SQLite**: Base de datos (desarrollo)
- **HTML/CSS**: Frontend

## Soporte

Para reportar problemas o solicitar nuevas funcionalidades, crea un issue en el repositorio.

## Licencia

Este proyecto es de uso privado.