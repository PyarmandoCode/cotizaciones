from django.shortcuts import redirect, render
from .models import Producto,Categoria,Umedida,Proveedor,Cliente,DetalleCotizacion,Cotizacion,Tipo_Cotizacion,Empresa,EstadoCotizacion
from django.http import JsonResponse,HttpResponse
from django.views.generic import  View

from django.db.models import Q,Max
from django.contrib.auth.models import User
from django.db import transaction

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth import authenticate,logout,login as auth_login
from django.urls import reverse
from django.contrib.auth.decorators import login_required



def Login(request):
    template_name = "Login.html"
    response_data = {}
    context = {}
    empresas=Empresa.objects.filter(state=True)
    if request.method == 'GET':
        context={
            "empresas":empresas
        }
        pass
    else:    
        if request.POST.get('action') == 'post':
            username = request.POST.get('usuario')
            password = request.POST.get('clave')
            empresa=request.POST.get('empresa')
            if len(empresa)>0:            
                nombre_empresa=Empresa.objects.get(id=empresa)
                user = authenticate(username=username, password=password)
                if user:
                    auth_login(request, user)
                    response_data['loggedin'] = True
                    response_data['username'] = user.first_name
                    response_data['completo'] = '{} {}'.format(user.first_name, user.last_name)
                    response_data['id'] = user.id
                    response_data['url'] = reverse('index_home')
                    request.session['usuario'] = '{} {}'.format(user.first_name, user.last_name)
                    request.session['loggedin'] = True
                    request.session['idempresa'] = empresa
                    request.session['empresa'] = nombre_empresa.nombre
                    request.session['logoempresa'] =nombre_empresa.logo_path
                    request.session['logoempresacotizacion'] =nombre_empresa.logo_path_cotizacion

                    response_data['msg'] = 'Bienvenido es un placer tenerlo por aca !!!'
                else:
                    response_data['loggedin'] = False
                    request.session['loggedin'] = False
                    response_data['msg'] = "Nombre de usuario o contraseña incorrecto!!!"
            else:
                 response_data['loggedin'] = False
                 request.session['loggedin'] = False
                 response_data['msg'] = "Seleccione una Empresa!!!"        
            return JsonResponse(response_data)
    return render(request, template_name,context)    

def Logoutapp(request):
    logout(request)
    return redirect('login')

def handler404(request, exception):
    context = {}
    response = render(request, "404.html", context=context)
    response.status_code = 404
    return response


def handler500(request):
    context = {}
    response = render(request, "500.html", context=context)
    response.status_code = 500
    return response

@login_required
def index(request):
    template_name="index.html"
    return render(request,template_name)

#region Productos
@login_required
def Productos_listado(request):
    productos = Producto.objects.filter(state=True)
    context = {
        "productos": productos,
    }
    template_name = "Listado_productos.html"
    return render(request, template_name, context)

@login_required
def Productos_visualizar(request,id):
    template_name = "Visualizar_productos.html"
    producto=Producto.objects.get(id=id)
    categoria=Categoria.objects.filter(state=True)
    proveedor=Proveedor.objects.filter(state=True)
    umedida=Umedida.objects.filter(state=True)
    
    #Seleccionado el color para mostrarla en el Combo
    categorias=Categoria.objects.get(id=producto.categoria.id)
    proveedores=Proveedor.objects.get(id=producto.proveedor.id)
    umedidas=Umedida.objects.get(id=producto.umedida.id)
    
    context = {"productos":producto,
               "Categorias":categoria,
               "Proveedores":proveedor,
               "Umedida":umedida,
               "categoriaseleccionado":categorias.nombre,
               "proveedorseleccionado":proveedores.nombre,
               "umedidaseleccionado":umedidas.nombre
               }
    return render(request, template_name,context)   

@login_required
def UpdateCrudProductos(request):
    response_data = {}
    template_name="Visualizar_productos.html"
    if request.POST.get('action') =='actualizar_productos':
        try:
            id=request.POST.get('id')
            productos = Producto.objects.get(id=id)
            productos.nombre=request.POST.get('txtnomprod')

            categoria_producto = request.POST.get('cmbcategoria')
            
            if categoria_producto=="":
                categoria=productos.categoria
            else:
                categoria=Categoria.objects.get(id=categoria_producto)
            productos.categoria=categoria

            productos.des_prod=request.POST.get('txtdescripcion')

            proveedor_producto = request.POST.get('cmbproveedores')
            if proveedor_producto =="":
                provee=productos.proveedor
            else:    
                provee=Proveedor.objects.get(id=proveedor_producto)
            productos.proveedor=provee

            productos.costo_real=request.POST.get('txtcostoreal')
            productos.costo_ofrecido=request.POST.get('txtcostofrecido')
            productos.ganancia=request.POST.get('txtganancia')

            umedida_producto = request.POST.get('cmbumedida')
            if umedida_producto =="":
                umedida=productos.umedida
            else:    
                umedida=Umedida.objects.get(id=umedida_producto)
            productos.umedida=umedida

            productos.save()
        except Exception as error:
            response_data['flag'] = False
            response_data['msg'] = f'No Se Modifico el Productos Correctamente {error}'
        else:
            response_data['flag'] = True
            response_data['msg'] = 'Se Modifico con exito el Producto'  
            
        return JsonResponse(response_data)   
    return render(request,template_name) 


class DeleteCrudProductos(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        Producto.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

@login_required    
def Productos_form(request):
    template_name = "Nuevo_productos.html"
    categoria=Categoria.objects.filter(state=True)
    proveedor=Proveedor.objects.filter(state=True)
    umedida=Umedida.objects.filter(state=True)
    context = {
        "Categorias":categoria,"Proveedores":proveedor,"Umedida":umedida
    }
    return render(request, template_name,context)   

@login_required
def CreateCrudProductos(request):
    response_data = {}
    template_name="Nuevo_productos.html"
    if request.POST.get('action') =='registrar_productos':
        try:
            nombre_producto = request.POST.get('txtnomprod')
            categoria_producto = request.POST.get('cmbcategoria')
            des_producto = request.POST.get('txtdescripcion')
            proveedor_producto = request.POST.get('cmbproveedores')
            costoreal = request.POST.get('txtcostoreal')
            costofrecido = request.POST.get('txtcostofrecido')
            ganancia = request.POST.get('txtganancia')
            unidadmedida_producto = request.POST.get('cmbumedida')
            categoria=Categoria.objects.get(id=categoria_producto)
            proveedor=Proveedor.objects.get(id=proveedor_producto)
            umedida=Umedida.objects.get(id=unidadmedida_producto)
            Producto.objects.create(nombre=nombre_producto,
                                      categoria=categoria,
                                      descripcion=des_producto,
                                      proveedor=proveedor,
                                      costo_real=costoreal,
                                      costo_ofrecido=costofrecido,
                                      ganancia=ganancia,
                                      umedida=umedida 
                                      )
            
        except Exception as error:
            response_data['flag'] = False
            response_data['msg'] = f'No se Registro el Servicio Correctamente {error}'
        else:
            response_data['flag'] = True
            response_data['msg'] = 'Se Registro con exito el Servicio'   
        return JsonResponse(response_data)   
    return render(request,template_name) 


class AutocompleteServicios(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query', '')
        items = Producto.objects.filter(Q(nombre__icontains=query))
        #suggestions = [item.nombre for item in items]
        suggestions = [{'nombre': item.nombre, 'id': item.pk } for item in items]
        return JsonResponse({'suggestions': suggestions})
    
  
#endregion Productos

#region Categorias
@login_required
def Categorias_listado(request):
    categorias = Categoria.objects.filter(state=True)
    context = {
        "Categorias": categorias,
    }
    template_name = "Listado_categorias.html"
    return render(request, template_name, context)

@login_required
def Categoria_form(request):
    template_name = "Nueva_categoria.html"
    return render(request, template_name)

@login_required
def CreateCrudCategorias(request):
    response_data = {}
    template_name="Nueva_categoria.html"
    if request.POST.get('action') =='registrar_categoria':
        try:
            nombre_categoria = request.POST.get('txtnomcat')
            Categoria.objects.create(nombre=nombre_categoria)
            
        except Exception as error:
            response_data['flag'] = False
            response_data['msg'] = f'No se Registro la Categoria Correctamente {error}'
        else:
            response_data['flag'] = True
            response_data['msg'] = 'Se Registro con exito la Categoria'   
        return JsonResponse(response_data)   
    return render(request,template_name) 

@login_required
def Categoria_visualizar(request,id):
    template_name = "Visualizar_categoria.html"
    categoria=Categoria.objects.get(id=id)
    context = {"categorias":
               categoria}
    return render(request, template_name,context)

@login_required
def UpdateCrudCategorias(request):
    response_data = {}
    template_name="Visualizar_categoria.html"
    if request.POST.get('action') =='actualizar_categoria':
        try:
            id=request.POST.get('id')
            categoria = Categoria.objects.get(id=id)
            categoria.nombre=request.POST.get('txtnomcat')
            categoria.save()
        except Exception as error:
            response_data['flag'] = False
            response_data['msg'] = f'No Se Modifico la Categoria Correctamente {error}'
        else:
            response_data['flag'] = True
            response_data['msg'] = 'Se Modifico con exito la Categoria'  
            
        return JsonResponse(response_data)   
    return render(request,template_name) 


class DeleteCrudCategorias(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        Categoria.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)
#endregion categorias    
    
#region Proveedores    
@login_required
def Proveedores_listado(request):
    proveedores = Proveedor.objects.filter(state=True)
    context = {
        "Proveedores": proveedores,
    }
    template_name = "Listado_proveedores.html"
    return render(request, template_name, context)    

@login_required
def Proveedor_form(request):
    template_name = "Nuevo_proveedor.html"
    return render(request, template_name)

@login_required
def CreateCrudProveedores(request):
    response_data = {}
    template_name="Nuevo_proveedor.html"
    if request.POST.get('action') =='registrar_proveedor':
        try:
            nombre_proveedor = request.POST.get('txtnomprov')
            ruc_proveedor = request.POST.get('txtrucprov')
            dir_proveedor = request.POST.get('txtdirprov')
            tlf_proveedor = request.POST.get('txttelprov')
            email_proveedor = request.POST.get('txtemailprov')
            contacto_proveedor = request.POST.get('txtcontactoprov')
            
            Proveedor.objects.create(nombre=nombre_proveedor,direccion=dir_proveedor,ruc=ruc_proveedor,telefono=tlf_proveedor,email=email_proveedor,contacto=contacto_proveedor)
            
        except Exception as error:
            response_data['flag'] = False
            response_data['msg'] = f'No se Registro El Proveedor Correctamente {error}'
        else:
            response_data['flag'] = True
            response_data['msg'] = 'Se Registro con exito El Proveedor'   
        return JsonResponse(response_data)   
    return render(request,template_name) 


class DeleteCrudProveedores(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        Proveedor.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

@login_required    
def Proveedor_visualizar(request,id):
    template_name = "Visualizar_proveedor.html"
    proveedor=Proveedor.objects.get(id=id)
    context = {"proveedor":proveedor
               }
    return render(request, template_name,context)   

@login_required
def UpdateCrudProveedor(request):
    response_data = {}
    template_name="Visualizar_proveedor.html"
    if request.POST.get('action') =='actualizar_proveedor':
        try:
            id=request.POST.get('id')
            proveedor = Proveedor.objects.get(id=id)
            proveedor.nombre=request.POST.get('txtnom')
            proveedor.ruc=request.POST.get('txtruc')
            proveedor.direccion=request.POST.get('txtdir')
            proveedor.telefono=request.POST.get('txtfono')
            proveedor.email=request.POST.get('txtemail')
            proveedor.contacto=request.POST.get('txtcontacto')
            proveedor.save()
        except Exception as error:
            response_data['flag'] = False
            response_data['msg'] = f'No Se Modifico el Proveedor Correctamente {error}'
        else:
            response_data['flag'] = True
            response_data['msg'] = 'Se Modifico con exito El Proveedor'  
            
             
        return JsonResponse(response_data)   
    return render(request,template_name)  
#endregion Proveedores   

#region Clientes
@login_required
def Clientes_listado(request):
    clientes = Cliente.objects.filter(state=True)
    context = {
        "Clientes": clientes,
    }
    template_name = "Listado_clientes.html"
    return render(request, template_name, context)   

@login_required
def Cliente_form(request):
    template_name = "Nuevo_cliente.html"
    return render(request, template_name)

@login_required
def CreateCrudClientes(request):
    response_data = {}
    template_name="Nuevo_cliente.html"
    if request.POST.get('action') =='registrar_cliente':
        try:
            nombre_cliente = request.POST.get('txtnomclie')
            ruc_cliente = request.POST.get('txtrucclie')
            dir_cliente = request.POST.get('txtdirclie')
            tlf_cliente = request.POST.get('txttelclie')
            email_cliente = request.POST.get('txtemailclie')
            contacto_cliente = request.POST.get('txtcontactoclie')
            
            Cliente.objects.create(nombre=nombre_cliente,direccion=dir_cliente,ruc=ruc_cliente,telefono=tlf_cliente,email=email_cliente,contacto=contacto_cliente)
            
        except Exception as error:
            response_data['flag'] = False
            response_data['msg'] = f'No se Registro El Cliente Correctamente {error}'
        else:
            response_data['flag'] = True
            response_data['msg'] = 'Se Registro con exito El Cliente'   
        return JsonResponse(response_data)   
    return render(request,template_name) 


class DeleteCrudClientes(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        Cliente.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

@login_required    
def Cliente_visualizar(request,id):
    template_name = "Visualizar_cliente.html"
    cliente=Cliente.objects.get(id=id)
    context = {"cliente":cliente
               }
    return render(request, template_name,context)   

@login_required
def UpdateCrudCliente(request):
    response_data = {}
    template_name="Visualizar_cliente.html"
    if request.POST.get('action') =='actualizar_cliente':
        try:
            id=request.POST.get('id')
            cliente = Cliente.objects.get(id=id)
            cliente.nombre=request.POST.get('txtnom')
            cliente.ruc=request.POST.get('txtruc')
            cliente.direccion=request.POST.get('txtdir')
            cliente.telefono=request.POST.get('txtfono')
            cliente.email=request.POST.get('txtemail')
            cliente.contacto=request.POST.get('txtcontacto')
            cliente.save()
        except Exception as error:
            response_data['flag'] = False
            response_data['msg'] = f'No Se Modifico el Cliente Correctamente {error}'
        else:
            response_data['flag'] = True
            response_data['msg'] = 'Se Modifico con exito El Cliente'  
            
             
        return JsonResponse(response_data)   
    return render(request,template_name)      

class AutocompleteClientes(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query', '')
        items = Cliente.objects.filter(Q(nombre__icontains=query))
        #suggestions = [item.nombre for item in items]
        suggestions = [{'nombre': item.nombre, 'ruc': item.ruc,'contacto':item.contacto,'id':item.pk} for item in items]
        return JsonResponse({'suggestions': suggestions})
    
#endregion Clientes   
    
@login_required
def Listar_cotizaciones(request):
    template_name="Listado_cotizaciones.html"
    cotizaciones=Cotizacion.objects.filter(state=True)#orm QUERYSET
    cotizaciones_ordenadas = cotizaciones.order_by('fecha_cotizacion')
    context = {
        "cotizaciones": cotizaciones_ordenadas,
    }
    return render(request,template_name,context)    

@login_required
def incrementar_detalle(request):
    # Inicializamos el contador en 0 si es la primera vez que se accede
    if 'contador' not in request.session:
        request.session['contador'] = 0
    # Incrementamos el contador en 1
    lstdetallecotizacion = request.session.get('lstdetallecotizacion', [])    
    request.session['contador'] =int(len(lstdetallecotizacion)+1)
    contador=request.session['contador']
    return contador

#ACA HAGO DOS COSAS ACTUALIZAR Y GRABAR EN LAS LISTAS EN MEMORIA
@login_required
def Grabar_item_cotizacion(request):
    response_data = {}
    lstdetallecotizacion = request.session.get('lstdetallecotizacion', [])
    template_name="cotizacion.html"
    if request.POST.get('action') =='registrar_cotizacion':
        try:
           
            iddetalle=request.POST.get('iddetalle')
            idservicio=request.POST.get('id_servicio')
            cotizacion=request.POST.get('numcotizacion')
            detalle = request.POST.get('detalle')
            precio = request.POST.get('precio')
            preciocompra = request.POST.get('preciocompra')
            cantidad = request.POST.get('cantidad')
            fechas = request.POST.get('fechas')
            total = request.POST.get('total')
            costocompra= request.POST.get('costocompra')
           
            if len(iddetalle)!=0:
                for indice in lstdetallecotizacion:
                    
                    if int(iddetalle)==int(indice["iddetalle"]):
                        
                        if len(idservicio)!=0:
                            objservicio=Producto.objects.get(pk=idservicio)
                            servicio = objservicio.nombre
                            id=idservicio
                            lstdetallecotizacion[int(iddetalle)-1]["idservicio"]=idservicio
                            lstdetallecotizacion[int(iddetalle)-1]["servicio"]=servicio
                        else:    
                            lstdetallecotizacion[int(iddetalle)-1]["detalle"]=detalle
                            lstdetallecotizacion[int(iddetalle)-1]["precio"]=precio
                            lstdetallecotizacion[int(iddetalle)-1]["preciocompra"]=preciocompra
                            lstdetallecotizacion[int(iddetalle)-1]["cantidad"]=cantidad
                            lstdetallecotizacion[int(iddetalle)-1]["fechas"]=fechas
                            lstdetallecotizacion[int(iddetalle)-1]["costo"]=total
                            lstdetallecotizacion[int(iddetalle)-1]["costocompra"]=costocompra
                        request.session['lstdetallecotizacion'] = lstdetallecotizacion
                        break
            else:
                
                objservicio=Producto.objects.get(pk=idservicio)
                servicio = objservicio.nombre
                id=idservicio
                item_detalle_cotizacion={
                            "iddetalle":int(incrementar_detalle(request)),
                            "cotizacion":cotizacion,
                            "idservicio":id,
                            "servicio":servicio,
                            "detalle":detalle,
                            "precio":precio,
                            "preciocompra":preciocompra,
                            "cantidad":cantidad,
                            "fechas":fechas,
                            "costo":total,
                            "costocompra":costocompra
                        }
                lstdetallecotizacion.append(item_detalle_cotizacion)
                # Guardar el diccionario en la sesión
                request.session['lstdetallecotizacion'] = lstdetallecotizacion
                
        except Exception as error:
            response_data['flag'] = False
            response_data['msg'] = f'No se Registro el Servicio Correctamente {error}'
        else:
            response_data['flag'] = True
            response_data['msg'] = 'Se Registro con exito el Servicio'  
        return JsonResponse(response_data)   
    return render(request,template_name) 

#ACA CREO LA COTIZACION EN LA BD CABECERA Y DETALLE
@login_required
def Cotizacion_crear(request,numcot,tipo,actualizar):
    response_data = {}
    context={}
    template_name="cotizacion.html"
    if request.method == 'GET':
        lstdetallecotizacion = request.session.get('lstdetallecotizacion', {})
        context = {
             "detalle": lstdetallecotizacion,
        }
    else:    
        if request.POST.get('action') =='registrar_cotizacion_cabecera':
            try:
                opciones=request.POST.get('opciones')
                if opciones=="1":
                    objtipo_cotizacion = Tipo_Cotizacion.objects.get(pk=1)
                else:
                    objtipo_cotizacion = Tipo_Cotizacion.objects.get(pk=2)
                nombre_evento = request.POST.get('evento')
                capacidad = request.POST.get('capacidad')
                lugar = request.POST.get('lugar')    
                numcotizacion= request.POST.get('numcotizacion')    
                idcliente = request.POST.get('idcliente')
                objcliente=Cliente.objects.get(id=idcliente)
                fecha_cotizacion = request.POST.get('fecha')
                comentario = request.POST.get('comentario')
                totalFee = request.POST.get('totalFee')
                mas_sin_igv=True
                obj_user=User.objects.get(pk=1)
                persona_creo_cotiza=obj_user
                total=request.POST.get('totalSubt')
                totalcompra=request.POST.get('totalcompra')
                obj_estado_cot=EstadoCotizacion.objects.get(pk=1)
                estado=obj_estado_cot
                codempresa=int(request.session.get('idempresa'))
                obj_empresa=Empresa.objects.get(pk=codempresa)
                con_que_empresa=obj_empresa
                lstdetallecotizacion = request.session.get('lstdetallecotizacion', [])
                
                item=grabar_cotizacion(lstdetallecotizacion, numcotizacion,objtipo_cotizacion,objcliente,nombre_evento,fecha_cotizacion,capacidad,lugar,comentario,totalFee,mas_sin_igv,persona_creo_cotiza,total,totalcompra,estado,con_que_empresa)
               
                if not item:
                    raise ValueError("Debe seleccionar por lo menos un Servicio")
                elif item!=True:
                    raise ValueError("Debe Ingresar todos los campos Correctamente")
            except ValueError as error:
                response_data['flag'] = False
                response_data['msg'] = f'Debe Ingresar todos los campos Correctamente {error} '       
            except Exception as error:
                response_data['flag'] = False
                response_data['msg'] = f'Debe Ingresar todos los campos Correctamente {error} '       
            else:
                response_data['flag'] = True
                response_data['msg'] = 'Se Registro con exito la Cotizacion'
                request.session['lstdetallecotizacion'] = []   
            return JsonResponse(response_data)   
       
    return render(request, template_name, context)



def grabar_cotizacion(data_items, numcot,tipocot,cliente,evento,fecha,capacidad,lugar,comentario,fee,mas_sin_igv,persona_creo_cotiza,total,totalcompra,estado,con_que_empresa):
    detalle_agregado = False  # Bandera para indicar si se ha agregado algún detalle
    try:
        # Comenzar una transacción
        with transaction.atomic():
            # Si hay registros en el diccionario, guardar los detalles de la cotización
            if data_items:
                 # Guardar el número de cotización en la cabecera
                Cotizacion.objects.create(nrocotizacion=numcot,
                        tipo_cotizacion=tipocot,
                        cliente=cliente,
                        nombre_evento=evento,
                        fecha_cotizacion=fecha,
                        capacidad=capacidad,
                        lugar=lugar,
                        comentario=comentario,
                        fee=fee,
                        mas_sin_igv=mas_sin_igv,
                        persona_creo_cotiza=persona_creo_cotiza,
                        total=total,
                        totalcompra=totalcompra,
                        estado=estado,
                        con_que_empresa=con_que_empresa)
                # Obtener la instancia de Cotizacion correspondiente a numcot
                cotizacion = Cotizacion.objects.get(pk=numcot)
                for item in data_items:
                    objservicio = Producto.objects.get(pk=item["idservicio"])
                    DetalleCotizacion.objects.create(
                        cotizacion=cotizacion,
                        servicio=objservicio,
                        detalle=item["detalle"],
                        precio=item["precio"],
                        preciocompra=item["preciocompra"],
                        cantidad=item["cantidad"],
                        fechas=item["fechas"],
                        costo=item["costo"],
                        costocompra=item["costocompra"]
                    )
                detalle_agregado = True  # Se ha agregado al menos un detalle    
        return detalle_agregado 
    except Exception as e:
        # Manejar errores de transacción
        print(f"Error al guardar la cotización: {e}")
        return f"Error al guardar la cotización: {e}"


@login_required
def Cancelar_cotizacion(request):
    template_name="cotizacion.html"
    if request.method == 'POST':
        if 'lstdetallecotizacion' in request.session:
            del request.session['lstdetallecotizacion']
            del request.session['contador']
            return redirect('listar_cotizaciones') 
    return render(request, template_name)    

@login_required
def Cotizacion_visualizar(request,numcot,tipo,actualizar):
    response_data = {}
    context={}
    template_name="cotizacion.html"
    if request.method == 'GET':
        
        cabeceracotizacion=Cotizacion.objects.get(pk=numcot)
        estado_cotizacion = cabeceracotizacion.estado.id
        #print(f"este es el estado de la coti {estado_cotizacion}")
        tipo_cot = actualizar
        
        lstdetallecotizacion = DetalleCotizacion.objects.filter(cotizacion=numcot,
        state=True)
        estadocotizacion=EstadoCotizacion.objects.all()

        context = {
             "detalle": lstdetallecotizacion,
             "cabecera":cabeceracotizacion,
             "estadocotizacion":estadocotizacion,
             'valor_bd': estado_cotizacion,
             "tipo_cot":tipo_cot
        }
       
       
    else:    
        if request.POST.get('action') =='registrar_cotizacion_cabecera':
            try:
                opciones=request.POST.get('opciones')
               
                if opciones=="1":
                    objtipo_cotizacion = Tipo_Cotizacion.objects.get(pk=1)
                else:
                    objtipo_cotizacion = Tipo_Cotizacion.objects.get(pk=2)
                nombre_evento = request.POST.get('evento')
                capacidad = request.POST.get('capacidad')
                lugar = request.POST.get('lugar')    
                numcotizacion= request.POST.get('numcotizacion')    
                idcliente = request.POST.get('idcliente')
                objcliente=Cliente.objects.get(id=idcliente)
                fecha_cotizacion = request.POST.get('fecha')
                comentario = request.POST.get('comentario')
                totalFee = request.POST.get('totalFee')
                mas_sin_igv=True
                user_logeado=response_data['id']
                obj_user=User.objects.get(pk=user_logeado)
                persona_creo_cotiza=obj_user
                total=request.POST.get('totalSubt')
                obj_estado_cot=EstadoCotizacion.objects.get(pk=1)
                estado=obj_estado_cot
                codempresa=int(request.session.get('idempresa'))
                obj_empresa=Empresa.objects.get(pk=codempresa)
                con_que_empresa=obj_empresa
                lstdetallecotizacion = request.session.get('lstdetallecotizacion', [])
               
                item=grabar_cotizacion(lstdetallecotizacion, numcotizacion,objtipo_cotizacion,objcliente,nombre_evento,fecha_cotizacion,capacidad,lugar,comentario,totalFee,mas_sin_igv,persona_creo_cotiza,total,estado,con_que_empresa)
                if not item:
                    raise ValueError("Debe seleccionar por lo menos un Servicio")
                elif item!=True:
                    raise ValueError("Debe Ingresar todos los campos Correctamente")
            except ValueError as error:
                response_data['flag'] = False
                response_data['msg'] = f'Debe Ingresar todos los campos Correctamente'       
            except Exception as error:
                response_data['flag'] = False
                response_data['msg'] = f'Debe Ingresar todos los campos Correctamente'       
            else:
                response_data['flag'] = True
                response_data['msg'] = 'Se Registro con exito la Cotizacion'
                request.session['lstdetallecotizacion'] = []   
            return JsonResponse(response_data)   
       
    return render(request, template_name, context)


class Eliminar_detalle_cotizacion(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        if 'lstdetallecotizacion' in request.session:
            # Obtén la lista de la sesión
            lstdetallecotizacion = request.session['lstdetallecotizacion']
            # Verifica si se proporcionó un índice válido en la solicitud POST
            indice_eliminar = int(id1) - 1
            # Elimina el elemento de la lista por su índice
            del lstdetallecotizacion[indice_eliminar]
            # Reasignar los índices de la lista
            #lstdetallecotizacionnueva = [elemento for elemento in lstdetallecotizacion]
            for index, detalle in enumerate(lstdetallecotizacion):
                detalle['iddetalle'] = index + 1
            # Actualiza la lista en la sesión
            request.session['lstdetallecotizacion'] = lstdetallecotizacion
            data = {
                'deleted': True
            }
            print("esta es la nueva lista regenerada")
            print(lstdetallecotizacion)
        return JsonResponse(data)
    
#ACA MODIFICO Y INSERTO UNA COTIZACION CUANDO YA ESTA GRABADO EN LA BD
@login_required
def modificar_item_cotizacion(request):
    response_data = {}
    template_name="cotizacion.html"
    if request.POST.get('action') =='actualizar_item_cotizacion':
        try:
            id=request.POST.get('iddetalle')
            if len(id)==0:
                 objservicio = Producto.objects.get(pk=request.POST.get('id_servicio'))
                 numcotizacion=request.POST.get('numcotizacion')
                 objcotizacion=Cotizacion.objects.get(pk=numcotizacion)
                 DetalleCotizacion.objects.create(
                        cotizacion=objcotizacion,
                        servicio=objservicio,
                        detalle=request.POST.get('detalle'),
                        precio=request.POST.get('precio'),
                        preciocompra=request.POST.get('preciocompra'),
                        cantidad=request.POST.get('cantidad'),
                        fechas=request.POST.get('fechas'),
                        costo=request.POST.get('total'),
                        costocompra=request.POST.get('costocompra')
                    )
            else: 
                detalle_cotizacion = DetalleCotizacion.objects.get(pk=id)
                servicio_cambiar=request.POST.get('id_servicio')
                if len(servicio_cambiar)!=0:
                    servicio=Producto.objects.get(pk=servicio_cambiar)
                    detalle_cotizacion.servicio=servicio
                detalle_cotizacion.detalle=request.POST.get('detalle')
                detalle_cotizacion.precio=request.POST.get('precio')
                detalle_cotizacion.preciocompra=request.POST.get('preciocompra')
                detalle_cotizacion.cantidad=request.POST.get('cantidad')
                detalle_cotizacion.fechas=request.POST.get('fechas')
                detalle_cotizacion.costo=request.POST.get('total')
                detalle_cotizacion.costocompra=request.POST.get('costocompra')
                detalle_cotizacion.save()
        except Exception as error:
            response_data['flag'] = False
            response_data['msg'] = f'No Se Modifico el Servicio Correctamente {error}'
        else:
            response_data['flag'] = True
            response_data['msg'] = 'Se Modifico con exito El Servicio'  
        return JsonResponse(response_data)   
    return render(request,template_name)          
    

class EliminarItemCotizacionBD(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        DetalleCotizacion.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)
    

class EliminarCotizacionBD(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        Cotizacion.objects.filter(nrocotizacion=id1).update(state=False)
        data = {
            'deleted': True
        }
        return JsonResponse(data)    

@login_required
def Actualizar_totales_bd(request):
    if request.method == 'POST' and request.POST.get('action') == 'actualizar_totales':
        try:
            numcotizacion= request.POST.get('numcotizacion')    
            idcliente = request.POST.get('idcliente')
            nombre_evento = request.POST.get('evento')
            capacidad = request.POST.get('capacidad')
            lugar = request.POST.get('lugar')    
            fecha_cotizacion = request.POST.get('fecha')
            comentario = request.POST.get('comentario')
            totalFee = request.POST.get('totalFee')
            totalSubt = request.POST.get('totalSubt')
            totalcompra = request.POST.get('totalcompra')
            estadocotizacion=request.POST.get('estadocotizacion')
            print(f"estadodecotizacionact {estadocotizacion}")

            coti = Cotizacion.objects.get(nrocotizacion=numcotizacion)
            if len(idcliente)>0:
                objcliente=Cliente.objects.get(id=idcliente)
                coti.cliente=objcliente
            coti.nombre_evento=nombre_evento
            coti.fecha_cotizacion=fecha_cotizacion
            coti.capacidad=capacidad
            coti.lugar=lugar
            coti.comentario=comentario
            coti.fee= totalFee
            coti.total = totalSubt
            coti.totalcompra = totalcompra
            objestadocot=EstadoCotizacion.objects.get(pk=estadocotizacion)
            coti.estado=objestadocot
            coti.save()
            response_data = {'flag': True, 'msg': 'Se actualizó con éxito'}
        except Exception as e:
            response_data = {'flag': False, 'msg': f'Error: {str(e)}'}
    else:
        response_data = {'flag': False, 'msg': 'Solicitud no válida'}
    return JsonResponse(response_data)

@login_required
def obtener_la_ultima_cotizacion(request):
    # Utiliza aggregate para obtener el valor máximo del campo Char
    valor_mas_alto = Cotizacion.objects.aggregate(max_valor=Max('nrocotizacion'))
    max_valor = valor_mas_alto['max_valor']
    return JsonResponse({'max_valor': max_valor})


@login_required
def visualizar_cotizacion(request,numcot):
     template_path="cotizacion_print.html"
     template = get_template(template_path)
     cabeceracotizacion=Cotizacion.objects.get(pk=numcot)
     lstdetallecotizacion = DetalleCotizacion.objects.filter(cotizacion=numcot,
        state=True)
     subtotal=cabeceracotizacion.total
     fee=cabeceracotizacion.fee
     total=float(subtotal) + float(fee)
     igv=float(total)*0.18
     total_ven=total+igv
     
     context = {
             "cabecera":cabeceracotizacion,
             "detalle": lstdetallecotizacion,
             "total":round(total,2),
             "igv" :round(igv,2),
             "total_ven":round(total_ven,2),
             "logopath":request.session.get('logoempresacotizacion')
        }
     #return render(request,template_path,context)

     
     html = template.render(context)
     response = HttpResponse(content_type='application/pdf')
     nombre_pdf=f"{numcot}.pdf"
     response['Content-Disposition'] = 'attachment; filename='+nombre_pdf

     pisa_status = pisa.CreatePDF(
        html, dest=response, encoding='utf-8')

     if pisa_status.err:
        return HttpResponse('Error al generar PDF: %s' % html)

     return response
    
    