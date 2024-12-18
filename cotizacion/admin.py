from django.contrib import admin

from .models import Producto,Proveedor,Umedida,Categoria,Cliente,Tipo_Cotizacion,Cotizacion,DetalleCotizacion,EstadoCotizacion,Empresa,Tipo_Venta,Venta,DetalleVenta,Compras,DetalleCompras

admin.site.site_header = "Panel de Administración - DNS"
admin.site.site_title = "DNS"
admin.site.index_title = "Bienvenido a DNS"


admin.site.register([Producto,Proveedor,Tipo_Venta,Venta,DetalleVenta,Compras,DetalleCompras,DetalleCotizacion,EstadoCotizacion,Empresa,Umedida,Categoria,Cliente,Tipo_Cotizacion,Cotizacion])
