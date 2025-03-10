from django.urls import path
from .views import index,Productos_listado,Productos_visualizar,DeleteCrudProductos,UpdateCrudProductos,Productos_form,CreateCrudProductos,Categorias_listado,Categoria_form,CreateCrudCategorias,UpdateCrudCategorias,Categoria_visualizar,DeleteCrudCategorias,Proveedores_listado,Proveedor_form,CreateCrudProveedores,DeleteCrudProveedores,Proveedor_visualizar,UpdateCrudProveedor,Cotizacion_crear,AutocompleteServicios,Clientes_listado,Cliente_form,CreateCrudClientes,DeleteCrudClientes,Cliente_visualizar,UpdateCrudCliente,AutocompleteClientes,Grabar_item_cotizacion,Listar_cotizaciones,Cancelar_cotizacion,Cotizacion_visualizar,Eliminar_detalle_cotizacion,modificar_item_cotizacion,EliminarItemCotizacionBD,Actualizar_totales_bd,EliminarCotizacionBD,obtener_la_ultima_cotizacion,visualizar_cotizacion,Login,Logoutapp,Listar_ventas,Cotizacion_a_Ventas,Visualizar_Venta,Listar_compras,Compra_crear,Grabar_item_compra,Eliminar_detalle_compra,Visualizar_Compra,EliminarItemComprasBD,Grabar_item_compraBD,actualizar_cabecera_compraBD,EliminarCompraBD,importar_excel_productos,cargar_productos_excel

def seleccionar_vista(request, *args, **kwargs):
    # Verifica si existe la variable de sesión 'opcion'
    if request.session.get('opcion') == 'create':
        return Eliminar_detalle_compra.as_view()(request, *args, **kwargs) 
    else:
        return EliminarItemComprasBD.as_view()(request, *args, **kwargs)
        

urlpatterns = [
    path('index_home/', index,name="index_home"),
    path('listado_productos/', Productos_listado,name="listado_productos"),
    path('productos_visualizar/<int:id>', Productos_visualizar,name="productos_visualizar"),
    path('productos_actualizar/', UpdateCrudProductos,name="productos_actualizar"),
    path('productos_eliminar/', DeleteCrudProductos.as_view(),name="productos_eliminar"),
    path('agregar_productos/', Productos_form,name="agregar_productos"),
    path('registrar_productos/', CreateCrudProductos,name="registrar_productos"),
    path('listado_categorias/', Categorias_listado,name="listado_categorias"),
     path('agregar_categorias/', Categoria_form,name="agregar_categoria"),
    path('registrar_categorias/', CreateCrudCategorias,name="registrar_categoria"),
    path('categoria_visualizar/<int:id>', Categoria_visualizar,name="categoria_visualizar"),
    path('categoria_actualizar/', UpdateCrudCategorias,name="categoria_actualizar"),
    path('categoria_eliminar/', DeleteCrudCategorias.as_view(),name="categoria_eliminar"),
    path('listado_proveedores/', Proveedores_listado,name="listado_proveedores"),
    path('agregar_proveedores/', Proveedor_form,name="agregar_proveedores"),
    path('registrar_proveedores/', CreateCrudProveedores,name="registrar_proveedores"),
    path('proveedor_eliminar/', DeleteCrudProveedores.as_view(),name="proveedor_eliminar"),
    path('proveedor_visualizar/<int:id>', Proveedor_visualizar,name="proveedor_visualizar"),
    path('proveedor_actualizar/', UpdateCrudProveedor,name="proveedor_actualizar"),
    path('cotizacion_crear/<int:numcot>/<int:tipo>/<int:actualizar>', Cotizacion_crear,name="cotizacion_crear"),
    path('autocomplete/', AutocompleteServicios.as_view(), name='autocomplete'),
    path('listado_clientes/', Clientes_listado,name="listado_clientes"),
    path('agregar_clientes/', Cliente_form,name="agregar_clientes"),
    path('registrar_clientes/', CreateCrudClientes,name="registrar_clientes"),
    path('cliente_eliminar/', DeleteCrudClientes.as_view(),name="cliente_eliminar"),
    path('cliente_visualizar/<int:id>', Cliente_visualizar,name="cliente_visualizar"),
    path('cliente_actualizar/', UpdateCrudCliente,name="cliente_actualizar"),
    path('autocompletecliente/', AutocompleteClientes.as_view(), name='autocompletecliente'),
    path('grabar_item_cotizacion/', Grabar_item_cotizacion, name='grabar_item_cotizacion'),
    path('listar_cotizaciones/', Listar_cotizaciones, name='listar_cotizaciones'),
    path('Cancelar_cotizacion/', Cancelar_cotizacion, name='cancelar_cotizacion'),
    path('Cotizacion_visualizar/<int:numcot>/<int:tipo>/<int:actualizar>', Cotizacion_visualizar, name='cotizacion_visualizar'),
    path('eliminar_detalle_cotizacion', Eliminar_detalle_cotizacion.as_view(),name="eliminar_detalle_cotizacion"),
    path('modificar_item_cotizacion', modificar_item_cotizacion,name="modificar_item_cotizacion"),
    path('eliminar_detalle_cotizacion_bd', EliminarItemCotizacionBD.as_view(),name="eliminar_detalle_cotizacion_bd"),
    path('actualizar_totales_bd', Actualizar_totales_bd,name="actualizar_totales_bd"),
    path('eliminar_cotizacion_bd', EliminarCotizacionBD.as_view(),name="eliminar_cotizacion_bd"),
    path('obtener_la_ultima_cotizacion/', obtener_la_ultima_cotizacion,name="obtener_la_ultima_cotizacion"),
    path('visualizar_cotizacion_imprimir/<int:numcot>', visualizar_cotizacion,name="visualizar_cotizacion_imprimir"),
    path('', Login,name="login"),
    path('logoutapp', Logoutapp,name="logoutapp"),
    path('accounts/login/', Login, name='login'),
    path('listar_ventas/', Listar_ventas, name='listar_ventas'),
    path('Cotizacion_a_Ventas/<int:numcot>/', Cotizacion_a_Ventas, name='Cotizacion_a_Ventas'),
    path('Visualizar_Venta/<int:nroventa>/', Visualizar_Venta, name='Visualizar_Venta'),
    path('listar_compras/', Listar_compras, name='listar_compras'),
    path('Compra_crear/', Compra_crear, name='Compra_crear'),
    path('Grabar_item_compra/', Grabar_item_compra, name='Grabar_item_compra'),
    #path('eliminar_detalle_compra', Eliminar_detalle_compra.as_view(),name="eliminar_detalle_compra"),
    path('Visualizar_Compra/<int:nrocompra>/', Visualizar_Compra, name='Visualizar_Compra'),
    path('ruta_dinamica/', seleccionar_vista, name='ruta_dinamica'),
    path('Grabar_item_compraBD/', Grabar_item_compraBD, name='Grabar_item_compraBD'),
    path('actualizar_cabecera_compraBD/', actualizar_cabecera_compraBD, name='actualizar_cabecera_compraBD'),
    path('eliminar_compra_bd', EliminarCompraBD.as_view(),name="eliminar_compra_bd"),
    path('importar_excel_productos/', importar_excel_productos, name='importar_excel_productos'),
    path('cargar_productos_excel/', cargar_productos_excel, name='cargar_productos_excel'),
    
]