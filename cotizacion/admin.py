from django.contrib import admin

from .models import Producto,Proveedor,Umedida,Categoria,Cliente,Tipo_Cotizacion,Cotizacion,DetalleCotizacion,EstadoCotizacion,Empresa

admin.site.register([Producto,Proveedor,Umedida,Categoria,Cliente,Tipo_Cotizacion,Cotizacion,DetalleCotizacion,EstadoCotizacion,Empresa])
