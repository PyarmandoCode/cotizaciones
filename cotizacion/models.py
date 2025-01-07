from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError

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
    imagen=models.ImageField(upload_to='imagenes/', blank=True, null=True)

    class Meta:
        db_table = 'Categoria'

    def __str__(self):
        return self.nombre    
    

class Producto(models.Model):
    codigo_interno=models.CharField(max_length=100,blank=True, null=True)
    codigo_barra=models.CharField(max_length=100,blank=True, null=True)
    nombre = models.CharField(max_length=200)
    categoria=models.ForeignKey(Categoria, models.DO_NOTHING,blank=True, null=True)
    descripcion=models.TextField(blank=True, null=True)
    proveedor=models.ForeignKey(Proveedor, models.DO_NOTHING,blank=True, null=True)
    #concepto=models.TextField(max_length=500,blank=True, null=True
    costo_real=models.DecimalField(max_digits=7, decimal_places=2)
    costo_ofrecido=models.DecimalField(max_digits=7, decimal_places=2)
    costo_mayoreo=models.DecimalField(max_digits=7, decimal_places=2,blank=True, null=True)
    ganancia=models.DecimalField(max_digits=7, decimal_places=2,blank=True, null=True)
    umedida=models.ForeignKey(Umedida, models.DO_NOTHING,blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    stock_minimo= models.PositiveIntegerField(default=0)
    stock_maximo= models.PositiveIntegerField(default=0)
    ubicacion=models.CharField(max_length=200,blank=True, null=True)
    imagen=models.ImageField(upload_to='imagenes/', blank=True, null=True)
    imagen_codigo_barras = models.ImageField(upload_to='codigos_barras/', blank=True, null=True)
    se_importo=models.BooleanField(default=False)#ESTE CAMPO ES IMPORTANTE PORQUE CUANDO ACTUALIZE EL
    #STOCK NO PODRE HACERLO DESDE COMPRAS DEBERA SE MANUALMENTE PORQUE SE IMPORTO Y NO HAY UN NUMERO
    #COMPRA ASOCIADO
    state = models.BooleanField(default=True)
    class Meta:
        db_table = 'Producto'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
    
    
    
    def save(self, *args, **kwargs):
        # Si el campo de código de barras no tiene valor, lo generamos automáticamente
        if self.codigo_barra and not self.imagen_codigo_barras:
            # Generamos el código de barras usando python-barcode
            codigo_barra = barcode.get_barcode_class('ean13')
            barcode_instance = codigo_barra(self.codigo_barra, writer=ImageWriter())
            
            # Creamos una imagen en memoria
            buffer = BytesIO()
            barcode_instance.write(buffer)
            
            # Creamos un archivo temporal para guardar la imagen
            filename = f'{self.codigo_barra}.png'
            self.imagen_codigo_barras.save(filename, ContentFile(buffer.getvalue()), save=False)
           
        super().save(*args, **kwargs)



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
    fecha_cotizacion=models.DateTimeField(blank=True, null=True)
    capacidad=models.CharField(max_length=200,blank=True, null=True)
    lugar=models.CharField(max_length=100,blank=True, null=True)
    comentario=models.TextField(blank=True, null=True)
    
    fee=models.DecimalField(max_digits=7, decimal_places=2,blank=True, null=True)
    mas_sin_igv=models.BooleanField()
    persona_creo_cotiza = models.ForeignKey(User, on_delete=models.CASCADE)
    total=models.DecimalField(max_digits=7, decimal_places=2,blank=True, null=True)
    totalcompra=models.DecimalField(max_digits=7, decimal_places=2,blank=True, null=True)
    ganancia=models.DecimalField(max_digits=7, decimal_places=2,blank=True, null=True)
    estado=models.ForeignKey(EstadoCotizacion, on_delete=models.CASCADE)
    con_que_empresa=models.ForeignKey(Empresa, on_delete=models.CASCADE)
    convertido_factura=models.BooleanField(default=False)
    state = models.BooleanField(default=True)

    class Meta:
        db_table = 'Cotizacion'
        ordering = ['-fecha_cotizacion']

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


    
class Tipo_Venta(models.Model):
    tipo = models.CharField(max_length=200)
    state = models.BooleanField(default=True)

    class Meta:
        db_table = 'Tipo_Venta'

    def __str__(self):
        return self.tipo    

  
class Venta(models.Model):
    nroventa=models.CharField(max_length=8,primary_key=True)
    nrodocumento=models.CharField(max_length=18,blank=True, null=True) #Factura,Boleta,ETC
    tipo_venta=models.ForeignKey(Tipo_Venta, models.DO_NOTHING,blank=True, null=True)
    nrocotizacion=models.CharField(max_length=8,blank=True, null=True)# Aca se guarda el numero de cotizacion con que se creo esa venta
    cliente=models.ForeignKey(Cliente, models.DO_NOTHING)
    fecha_venta=models.DateField(blank=True, null=True)
    comentario=models.TextField(blank=True, null=True)
    persona_creo_venta = models.ForeignKey(User, on_delete=models.CASCADE)
    total_neto=models.DecimalField(max_digits=7, decimal_places=2,blank=True, null=True)
    total_igv=models.DecimalField(max_digits=7, decimal_places=2,blank=True, null=True)
    total_descuento=models.DecimalField(max_digits=7, decimal_places=2,blank=True, null=True,default=0.0)
    con_que_empresa=models.ForeignKey(Empresa, on_delete=models.CASCADE)
    state = models.BooleanField(default=True)

    class Meta:
        db_table = 'Venta'
        ordering = ['-fecha_venta']

    def __str__(self):
        return self.nroventa

class DetalleVenta(models.Model):
    venta=models.ForeignKey(Venta,models.DO_NOTHING)
    producto=models.ForeignKey(Producto, models.DO_NOTHING)
    cantidad=models.IntegerField()
    detalle=models.TextField(max_length=500,blank=True, null=True)
    state = models.BooleanField(default=True)

    class Meta:
        db_table = 'DetalleVenta'

    def __str__(self):
        return f'{self.id}'


class Compras(models.Model):
    numero_compra = models.CharField(max_length=50, unique=True)
    numero_documento = models.CharField(max_length=50,blank=True, null=True)
    fecha = models.DateTimeField()
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    detalle=models.TextField(max_length=500,blank=True, null=True)
    persona_creo_venta = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    con_que_empresa=models.ForeignKey(Empresa, on_delete=models.CASCADE,blank=True, null=True)
    state = models.BooleanField(default=True)

    def __str__(self):
        return f'Compra {self.numero_compra} - {self.proveedor}'

    class Meta:
        db_table = 'Compras'
        ordering = ['-fecha']
        verbose_name = 'Compras'
        verbose_name_plural = 'Compras'

    
class DetalleCompras(models.Model):
    compra = models.ForeignKey(Compras, on_delete=models.CASCADE)
    producto=models.ForeignKey(Producto, models.DO_NOTHING)
    cantidad = models.IntegerField(default=0)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.producto} - {self.cantidad} unidades'

    class Meta:
        db_table = 'DetalleCompras'
        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalles de Compra'



