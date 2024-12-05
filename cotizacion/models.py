from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save

class Empresa(models.Model):
    nombre = models.CharField(max_length=200)
    ruc = models.CharField(max_length=20)
    email=models.CharField(max_length=100, blank=True, null=True)
    logo_path = models.CharField(max_length=400, blank=True, null=True)
    logo_path_cotizacion = models.CharField(max_length=400, blank=True, null=True)
    state = models.BooleanField(default=True)

    class Meta:
        db_table = 'Empresa'

    def __str__(self):
        return self.nombre
    

class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    ruc = models.CharField(max_length=20)
    direccion=models.CharField(max_length=150, blank=True, null=True)
    email=models.CharField(max_length=100, blank=True, null=True)
    telefono=models.CharField(max_length=100, blank=True, null=True)
    contacto = models.CharField(max_length=200, blank=True, null=True)
    state = models.BooleanField(default=True)

    class Meta:
        db_table = 'Proveedor'

    def __str__(self):
        return self.nombre
    
class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    ruc = models.CharField(max_length=20)
    direccion=models.CharField(max_length=150, blank=True, null=True)
    email=models.CharField(max_length=100, blank=True, null=True)
    telefono=models.CharField(max_length=100, blank=True, null=True)
    contacto = models.CharField(max_length=200, blank=True, null=True)
    state = models.BooleanField(default=True)

    class Meta:
        db_table = 'Cliente'

    def __str__(self):
        return self.nombre    
    

class Umedida(models.Model):
    nombre = models.CharField(max_length=200)
    state = models.BooleanField(default=True)

    class Meta:
        db_table = 'Umedida'

    def __str__(self):
        return self.nombre
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    state = models.BooleanField(default=True)

    class Meta:
        db_table = 'Categoria'

    def __str__(self):
        return self.nombre    
    

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    categoria=models.ForeignKey(Categoria, models.DO_NOTHING,blank=True, null=True)
    descripcion=models.TextField(blank=True, null=True)
    proveedor=models.ForeignKey(Proveedor, models.DO_NOTHING)
    #concepto=models.TextField(max_length=500,blank=True, null=True
    costo_real=models.DecimalField(max_digits=7, decimal_places=2)
    costo_ofrecido=models.DecimalField(max_digits=7, decimal_places=2)
    ganancia=models.DecimalField(max_digits=7, decimal_places=2)
    umedida=models.ForeignKey(Umedida, models.DO_NOTHING)
    state = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)
    class Meta:
        db_table = 'Producto'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre



class EstadoCotizacion(models.Model):
    Estado=models.CharField(max_length=20)
    state = models.BooleanField(default=True)

    class Meta:
        db_table = 'EstadoCotizacion'

    def __str__(self):
        return self.Estado
    

class Tipo_Cotizacion(models.Model):
    tipo = models.CharField(max_length=200)
    state = models.BooleanField(default=True)

    class Meta:
        db_table = 'Tipo_Cotizacion'

    def __str__(self):
        return self.tipo


class Cotizacion(models.Model):
    nrocotizacion=models.CharField(max_length=8,primary_key=True)
    tipo_cotizacion=models.ForeignKey(Tipo_Cotizacion, models.DO_NOTHING,blank=True, null=True)

    cliente=models.ForeignKey(Cliente, models.DO_NOTHING)
    nombre_evento=models.CharField(max_length=200,blank=True, null=True)
    fecha_cotizacion=models.DateField(blank=True, null=True)
    capacidad=models.CharField(max_length=200,blank=True, null=True)
    lugar=models.CharField(max_length=100,blank=True, null=True)
    comentario=models.TextField(blank=True, null=True)
    
    fee=models.DecimalField(max_digits=7, decimal_places=2)
    mas_sin_igv=models.BooleanField()
    persona_creo_cotiza = models.ForeignKey(User, on_delete=models.CASCADE)
    total=models.DecimalField(max_digits=7, decimal_places=2,blank=True, null=True)
    totalcompra=models.DecimalField(max_digits=7, decimal_places=2,blank=True, null=True)
    ganancia=models.DecimalField(max_digits=7, decimal_places=2,blank=True, null=True)
    estado=models.ForeignKey(EstadoCotizacion, on_delete=models.CASCADE)
    con_que_empresa=models.ForeignKey(Empresa, on_delete=models.CASCADE)
    state = models.BooleanField(default=True)

    class Meta:
        db_table = 'Cotizacion'
        ordering = ['fecha_cotizacion']

    def __str__(self):
        return self.nrocotizacion
    
@receiver(pre_save, sender=Cotizacion)
def calcular_ganancia(sender, instance, **kwargs):
    # Convertir los valores de total y totalcompra a números
    try:
        total = float(instance.total)
        totalcompra = float(instance.totalcompra)
    except ValueError:
        # Manejar el caso en el que los valores no puedan ser convertidos a números
        raise ValueError("Los campos 'total' y 'totalcompra' deben ser números válidos.")

    # Calcular la ganancia
    instance.ganancia = total - totalcompra
    

class DetalleCotizacion(models.Model):
    cotizacion=models.ForeignKey(Cotizacion,models.DO_NOTHING)
    servicio=models.ForeignKey(Producto, models.DO_NOTHING)
    proveedor=models.ForeignKey(Proveedor, models.DO_NOTHING,blank=True, null=True)
    detalle=models.TextField(max_length=500,blank=True, null=True)
    precio=models.DecimalField(max_digits=7, decimal_places=2,blank=True, null=True) 
    preciocompra=models.DecimalField(max_digits=7, decimal_places=2,blank=True, null=True) 
    cantidad=models.IntegerField()
    fechas=models.IntegerField(null=True,blank=True)
    costo=models.DecimalField(max_digits=7, decimal_places=2,blank=True, null=True)
    costocompra=models.DecimalField(max_digits=7, decimal_places=2,blank=True, null=True)
    state = models.BooleanField(default=True)

    class Meta:
        db_table = 'DetalleCotizacion'

    def __str__(self):
        return self.cotizacion_id

    
class OrdenCompra(models.Model):
    nroorden=models.CharField(max_length=8,primary_key=True)
    cotizacion=models.ForeignKey(Cotizacion, models.DO_NOTHING)
    fecha_orden=models.DateField()
    nrofactura=models.CharField(max_length=8,blank=True, null=True)
    fecha_factura=models.DateField(blank=True, null=True)
    fecha_vencimiento=models.DateField(blank=True, null=True)
    tipo_facturacion=models.CharField(max_length=8,blank=True, null=True)
    concepto=models.TextField(blank=True, null=True)
    monto=models.DecimalField(max_digits=7, decimal_places=2)
    monto_con_igv=models.DecimalField(max_digits=7, decimal_places=2)
    monto_sin_igv=models.DecimalField(max_digits=7, decimal_places=2)
    termino_dias=models.IntegerField()
    pago=models.BooleanField()
    comentario=models.TextField(blank=True, null=True)
    state = models.BooleanField(default=True)

    class Meta:
        db_table = 'OrdenCompra'

    def __str__(self):
        return self.cotizacion

#este cambio es para los modelos

class Compra(models.Model):
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE)
    fecha_compra = models.DateField()
    

    def calcular_total(self):
        # Suma los subtotales de los detalles relacionados con esta compra
        return sum(detalle.subtotal for detalle in self.detalles.all())

    calcular_total.short_description = "Total"  # Etiqueta para mostrar en el admin

    
    def __str__(self):
        return f"Compra {self.id} - {self.proveedor.nombre}"
    
class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    def save(self, *args, **kwargs):
        # Verificamos si se está actualizando el detalle
        if self.pk:
            detalle_original = DetalleCompra.objects.get(pk=self.pk)
            diferencia_cantidad = self.cantidad - detalle_original.cantidad
        else:
            diferencia_cantidad = self.cantidad

        # Actualiza el subtotal
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

        # Actualiza el stock del producto
        self.producto.stock += diferencia_cantidad
        self.producto.save()
 
    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} x {self.precio_unitario}"

  
    # def save(self, *args, **kwargs):
    #     # Actualizar el stock al crear o actualizar un detalle de compra
    #     self.calcular_subtotal()
        
        # Actualizamos el stock del producto
        #self.producto.actualizar_stock(self.cantidad)

        #super(DetalleCompra, self).save(*args, **kwargs)

    # def __str__(self):
    #     return f"Detalle {self.id} - {self.producto.nombre}"    






