from django.contrib import admin

from .models import Producto,Proveedor,Umedida,Categoria,Cliente,Tipo_Cotizacion,Cotizacion,DetalleCotizacion,EstadoCotizacion,Empresa,Compra,DetalleCompra

admin.site.site_header = "Panel de Administración - DNS"
admin.site.site_title = "DNS"
admin.site.index_title = "Bienvenido a DNS"

class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    extra = 1  # Número de formularios vacíos que se mostrarán al inicio

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'costo_real', 'stock')
    search_fields = ('nombre',)
    list_filter = ('costo_real',)

class CompraAdmin(admin.ModelAdmin):
    inlines = [DetalleCompraInline]
    list_display = ('proveedor', 'fecha_compra', 'calcular_total')  # Usamos el método aquí
    search_fields = ('proveedor__nombre',)

class DetalleCompraAdmin(admin.ModelAdmin):
    list_display = ('compra', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    list_filter = ('compra', 'producto')
    search_fields = ('producto__nombre',)


class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono')
    search_fields = ('nombre',)

# Registrar los modelos en el admin

admin.site.register([Umedida,Categoria,Cliente,Tipo_Cotizacion,Cotizacion,DetalleCotizacion,EstadoCotizacion,Empresa])

admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Compra, CompraAdmin)
admin.site.register(DetalleCompra, DetalleCompraAdmin)
