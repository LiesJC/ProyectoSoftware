from django.urls import path
from django.conf import settings
from django.contrib.staticfiles.urls import static
from . import views 

urlpatterns  = [
    #Pagina Principal
    path('extra',views.principal,name="main"),                                                  #PAGINA DE PRUEBA
    path('',views.principal2,name="PRINCIPAL"),                                                 #PESTAÑA INICIAL
    path('acercaNosotros',views.informacion,name="INFORMACION"),  
    path('pedidos',views.pedidos,name="PEDIDOS"),  
    path('documentos',views.documentos,name="DOCUMENTOS"),  
    path('verProductos',views.verProductos,name="VER"),  
    
    #Productos
    path('inventario',views.listaProductos,name="PRODUCTOS"),                                   #PESTAÑA DE INVENTARIO
    path('eliminarProd/<int:idd>',views.eliminarProductos,name="ELIMINAR_PRODUCTOS"),           #PESTAÑA ELIMINACION DE PRODUCTO
    path('modificarProd/<int:idd>',views.modificarProductos,name="MODIFICAR_PRODUCTOS"),        #PESTAÑA MODIFICACION DE PRODUCTO
    path('crearProd',views.crearProductos,name="CREAR_PRODUCTOS"),                              #PESTAÑA CREACION DE PRODUCTO
    path('productos/repproductos',views.generar_pdf_productos,name="REPORTE_PDF_PROD"),         #PESTAÑA REPORTE DE PRODUCTO    
    path('productos/vistaprevia',views.vista_previa_productos,name="REPORTE_VISTA_PROD"),       #VISTA PREVIA DE PRODUCTO
    
    #Personal
    path('personal',views.listaPersonal,name="PERSONAL"), 
    path('eliminarPesonal/<int:idd>',views.eliminarPersonal,name="ELIMINAR_PERSONAL"),         #PESTAÑA ELIMINACION DE PERSONAL
    path('modificarPersonal/<int:idd>',views.modificarPersonal,name="MODIFICAR_PERSONAL"),     #PESTAÑA MODIFICACION DE PERSONAL
    path('añadirPersonal',views.añadirPersonal,name="AÑADIR_PERSONAL"),                         #PESTAÑA CREACION DE PERSONAL
    path('personal/repproductos',views.generar_pdf_personal,name="REPORTE_PDF_PERS"),         #PESTAÑA REPORTE DE PERSONAL   
    path('personal/vistaprevia',views.vista_previa_personal,name="REPORTE_VISTA_PERS"),       #VISTA PREVIA DE PERSONAL
    
    #Cliente
    path('clientes',views.listaCliente,name="CLIENTE"), 
    path('eliminarCliente/<int:idd>',views.eliminarCliente,name="ELIMINAR_CLIENTE"),           #PESTAÑA ELIMINACION DE PERSONAL
    path('modificarCliente/<int:idd>',views.modificarCliente,name="MODIFICAR_CLIENTE"),        #PESTAÑA MODIFICACION DE PERSONAL
    path('añadirCliente',views.añadirCliente,name="AÑADIR_CLIENTE"),                           #PESTAÑA CREACION DE PERSONAL
    path('cliente/repproductos',views.generar_pdf_cliente,name="REPORTE_PDF_CLIENTE"),         #PESTAÑA REPORTE DE PERSONAL   
    path('cliente/vistaprevia',views.vista_previa_cliente,name="REPORTE_VISTA_CLIENTE"),       #VISTA PREVIA DE PERSONAL

    #Proveedor
    path('Proveedor',views.listaProveedor,name="PROVEEDOR"), 
    path('eliminarProveedor/<int:idd>',views.eliminarProveedor,name="ELIMINAR_PROVEEDOR"),           #PESTAÑA ELIMINACION DE PERSONAL
    path('modificarProveedor/<int:idd>',views.modificarProveedor,name="MODIFICAR_PROVEEDOR"),        #PESTAÑA MODIFICACION DE PERSONAL
    path('añadirProveedor',views.añadirProveedor,name="AÑADIR_PROVEEDOR"),                           #PESTAÑA CREACION DE PERSONAL
    path('proveedor/repproductos',views.generar_pdf_proveedor,name="REPORTE_PDF_PROV"),         #PESTAÑA REPORTE DE PERSONAL   
    path('provedor/vistaprevia',views.vista_previa_proveedor,name="REPORTE_VISTA_PROV"),       #VISTA PREVIA DE PERSONAL

    #Login
    path('login/',views.loginP,name="LOGIN"),                                                   #PESTAÑA DE INGRESO AL SISTEMA
    path('logout/',views.logoutP,name="LOGOUT"),                                                #PESTAÑA DE SALIDA DEL SISTEMA

    #Ventas
    path('venta/ventaProd',views.ventas,name="VENTAS"),                                         #PESTAÑAS DE VENTAS
    path('venta_exitosa/<int:venta_id>/',views.ver_venta_exitosa,name="venta_exitosa"),         #PESTAÑA DE CONFIRMACION DE VENTA
    path('ventas/pdf/<int:venta_id>/', views.generar_pdf_venta, name='reporte_pdf_venta'),      #VENTA DE REPORTE DE VENTA
    path('ventas/listado/',views.listado_ventas, name='listado_ventas'),                        #LISTADO DE VENTAS 

    #Vision Artificial
    path('visionArtificial/camara',views.camara,name="CAMARA"),  
    path('camara/stream/', views.camara_red, name='CAMARA_RED'),
    path('camara/consulta/', views.consultafirebase, name='CONSULTA_FIREBASE'),
    path("toggle_vision/", views.toggle_vision, name="toggle_vision"),

    #Administrador de trabajos
    path('trabajos/pagina_tecnica', views.principal_tecnica, name='PAGINA_TECNICA'),
    path('trabajos/trabajos_tecnica', views.trabajos_tecnica, name='TRABAJOS_TECNICA'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#RUTA(rutadespuesdeldominio, vista de referencia, NombreURL)