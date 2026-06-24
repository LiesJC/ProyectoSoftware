from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import *
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
import json

from django.db.models import Q
# Create your views here.

from django.shortcuts import render, redirect
from sistema.basefirebase.firebase import *

from django.contrib.auth.decorators import login_required

# PAGINAS PRINCIPALES
def principal(request):
    return render(request,"pagina_principal/principal.html")            #RENDER RETORNO DE PAGINA(respuesta, ruta de pagina, {varaibles_prod})
def principal2(request):
    return render(request,"pagina_principal/menu_inicial.html")          
def informacion(request):
    return render(request, "pagina_principal/informacion_empresa.html")
def pedidos(request):
    return render(request, "pagina_principal/pedidos.html")
def documentos(request):
    return render(request, "pagina_principal/documentos.html")

def verProductos(request):
    # Capturar lo que el usuario busca en el buscador
    query = request.GET.get('buscar', '')
    # Capturar la categoría seleccionada
    categoria_seleccionada = request.GET.get('categoria', '')
    # Obtener todas las categorías únicas
    categorias = productos.objects.values_list('categoria', flat=True).distinct()
    # Filtrar productos
    productos_filtrados = productos.objects.all()
    if query:
        # Filtrar por descripción (buscador)
        productos_filtrados = productos_filtrados.filter(descripcion__icontains=query)
    if categoria_seleccionada and categoria_seleccionada != "Todos":
        # Filtrar por categoría seleccionada
        productos_filtrados = productos_filtrados.filter(categoria=categoria_seleccionada)
    return render(
        request,
        "pagina_principal/VerProductos.html",
        {
            "productos": productos_filtrados,
            "categorias": categorias,
            "categoria_seleccionada": categoria_seleccionada,
            "buscar": query
        }
    )

#RELACIONADO CON PRODUCTOS
@login_required(login_url='LOGIN')
def listaProductos(request):
    listaproductos = productos.objects.all()
    return render(request,"productos/listarProd.html",{"productos":listaproductos})

@login_required(login_url='LOGIN')
def eliminarProductos(request,idd):
    prod =  productos.objects.get(id=idd)
    prod.delete()
    return redirect("PRODUCTOS")

@login_required(login_url='LOGIN')
def modificarProductos(request,idd):
    prod = productos.objects.get(id=idd)
    formulario = ProductoForm(request.POST or None, request.FILES or None, instance=prod)
    if request.method =='POST':
        if formulario.is_valid():
            formulario.save()
            return redirect("PRODUCTOS")
    return render(request,"productos/modificarProd.html", {"formulario":formulario})






@login_required(login_url='LOGIN')
def crearProductos(request):
    formulario = ProductoForm(request.POST or None, request.FILES or None, prefix="prod")
    
    if formulario.is_valid():
        from .models import productos
        
        descripcion = formulario.cleaned_data.get('descripcion')
        precio = formulario.cleaned_data.get('precio')
        cantidad = formulario.cleaned_data.get('cantidad')
        stockmaximo = formulario.cleaned_data.get('stockmaximo')
        categoria = formulario.cleaned_data.get('categoria')
        marca = formulario.cleaned_data.get('marca')
        
        # Validaciones personalizadas
        if productos.objects.filter(descripcion__iexact=descripcion).exists():
            messages.error(request, f"⚠️ Ya existe un producto con la descripción '{descripcion}'")
            return render(request, "productos/crearProd.html", {"formulario": formulario})
        
        if not descripcion or len(descripcion.strip()) == 0:
            messages.error(request, "⚠️ La descripción es obligatoria")
            return render(request, "productos/crearProd.html", {"formulario": formulario})
        
        if precio <= 0:
            messages.error(request, "⚠️ El precio debe ser mayor a 0")
            return render(request, "productos/crearProd.html", {"formulario": formulario})
        
        if cantidad < 0:
            messages.error(request, "⚠️ La cantidad no puede ser negativa")
            return render(request, "productos/crearProd.html", {"formulario": formulario})
        
        if stockmaximo < 0:
            messages.error(request, "⚠️ El stock máximo no puede ser negativo")
            return render(request, "productos/crearProd.html", {"formulario": formulario})
        
        if not categoria or len(categoria.strip()) == 0:
            messages.error(request, "⚠️ La categoría es obligatoria")
            return render(request, "productos/crearProd.html", {"formulario": formulario})
        
        if not marca or len(marca.strip()) == 0:
            messages.error(request, "⚠️ La marca es obligatoria")
            return render(request, "productos/crearProd.html", {"formulario": formulario})
        
        try:
            producto = formulario.save()
            messages.success(request, f"✅ Producto '{producto.descripcion}' creado exitosamente")
            return redirect("PRODUCTOS")
        except Exception as e:
            messages.error(request, f"❌ Error al guardar: {str(e)}")
            return render(request, "productos/crearProd.html", {"formulario": formulario})
    
    else:
        # ========== MOSTRAR TODOS LOS ERRORES DEL FORMULARIO ==========
        for field, errors in formulario.errors.items():
            for error in errors:
                # Mostrar cada error con messages
                messages.error(request, f"⚠️ {field}: {error}")
        
        # También mostrar errores en el contexto
        return render(request, "productos/crearProd.html", {
            "formulario": formulario,
            "errores_formulario": formulario.errors  # 👈 PASAR ERRORES AL TEMPLATE
        })
    
    return render(request, "productos/crearProd.html", {"formulario": formulario})




@login_required(login_url='LOGIN')
def generar_pdf_productos(request):
    productoss = productos.objects.all()
    template = get_template("productos/reporte_productos.html")

    context = {
        'productos': productoss,
        'fecha': datetime.now(),
        'reporte': True  # 👈 ESTA LÍNEA es la clave
    }
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment;filename = "reporte_productos.pdf"'
    pisa_status=pisa.CreatePDF(html,dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar PDF', status = 500)
    return response

@login_required(login_url='LOGIN')
def vista_previa_productos(request):
    productoss = productos.objects.all()
    return render(request, 'productos/reporte_productos.html',{'productos':productoss,'fecha': datetime.now(),"reporte": True})

#RELACIONADO CON PERSONAL
@login_required(login_url='LOGIN')
def listaPersonal(request):
    lista_personal = Empleado.objects.all()
    return render(request,"personal/listarPersonal.html",{"empleados":lista_personal})

@login_required(login_url='LOGIN')
def eliminarPersonal(request,idd):
    prod =  Empleado.objects.get(id=idd)
    prod.delete()
    return redirect("PERSONAL")

@login_required(login_url='LOGIN')
def modificarPersonal(request,idd):
    prod = Empleado.objects.get(id=idd)
    formulario = EmpleadoForm(request.POST or None, request.FILES or None, instance=prod)
    if request.method =='POST':
        if formulario.is_valid():
            formulario.save()
            return redirect("PERSONAL")
    return render(request,"personal/modificarPersonal.html", {"formulario":formulario})

@login_required(login_url='LOGIN')
def añadirPersonal(request):
    formulario = EmpleadoForm(request.POST or None, request.FILES or None,prefix="pers")
    if formulario.is_valid():
        formulario.save()
        return redirect("PERSONAL")
    else:
        print("Error en el formulario")
        print(formulario.errors)
    return render(request,"personal/añadirPersonal.html",{"formulario":formulario})

@login_required(login_url='LOGIN')
def generar_pdf_personal(request):
    personal = Empleado.objects.all()
    template = get_template("personal/reporte_personal.html")

    context = {
        'personal': personal,
        'fecha': datetime.now(),
        'reporte': True  # 👈 ESTA LÍNEA es la clave
    }
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment;filename = "reporte_personal.pdf"'
    pisa_status=pisa.CreatePDF(html,dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar PDF', status = 500)
    return response

@login_required(login_url='LOGIN')
def vista_previa_personal(request):
    personal = Empleado.objects.all()
    return render(request, 'personal/reporte_personal.html',{'personal':personal,'fecha': datetime.now(),"reporte": True})

#RELACIONADO CON CLIENTE
@login_required(login_url='LOGIN')
def listaCliente(request):
    listaproductos = clientes.objects.all()
    return render(request,"clientes/listarCliente.html",{"clientes":listaproductos})

@login_required(login_url='LOGIN')
def eliminarCliente(request,idd):
    prod =  clientes.objects.get(id=idd)
    prod.delete()
    return redirect("CLIENTE")

@login_required(login_url='LOGIN')
def modificarCliente(request,idd):
    prod = clientes.objects.get(id=idd)
    formulario = ClienteForm(request.POST or None, request.FILES or None, instance=prod)
    if request.method =='POST':
        if formulario.is_valid():
            formulario.save()
            return redirect("CLIENTE")
    return render(request,"clientes/modificarCliente.html", {"formulario":formulario})

@login_required(login_url='LOGIN')
def añadirCliente(request):
    formulario = ClienteForm(request.POST or None, request.FILES or None,prefix="cliente")
    if formulario.is_valid():
        formulario.save()
        return redirect("CLIENTE")
    else:
        print("Error en el formulario")
        print(formulario.errors)
    return render(request,"clientes/añadirCliente.html",{"formulario":formulario})

@login_required(login_url='LOGIN')
def generar_pdf_cliente(request):
    cliente = clientes.objects.all()
    template = get_template("clientes/reporte_clientes.html")

    context = {
        'clientes': cliente,
        'fecha': datetime.now(),
        'reporte': True  # 👈 ESTA LÍNEA es la clave
    }
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment;filename = "reporte_clientes.pdf"'
    pisa_status=pisa.CreatePDF(html,dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar PDF', status = 500)
    return response

@login_required(login_url='LOGIN')
def vista_previa_cliente(request):
    cliente = clientes.objects.all()
    return render(request, 'clientes/reporte_clienteS.html',{'clientes':cliente,'fecha': datetime.now(),"reporte": True})

#RELACIONADO CON PROVEEDOR 
@login_required(login_url='LOGIN')
def listaProveedor(request):
    listaproductos = proveedor.objects.all()
    return render(request,"proveedores/listarProveedor.html",{"proveedores":listaproductos})

@login_required(login_url='LOGIN')
def eliminarProveedor(request,idd):
    prod =  proveedor.objects.get(id=idd)
    prod.delete()
    return redirect("PROVEEDOR")

@login_required(login_url='LOGIN')
def modificarProveedor(request,idd):
    prod = proveedor.objects.get(id=idd)
    formulario = ProveedorForm(request.POST or None, request.FILES or None, instance=prod)
    if request.method =='POST':
        if formulario.is_valid():
            formulario.save()
            return redirect("PROVEEDOR")
    return render(request,"proveedores/modificarProveedor.html", {"formulario":formulario})

@login_required(login_url='LOGIN')
def añadirProveedor(request):
    formulario = ProveedorForm(request.POST or None, request.FILES or None,prefix="prov")
    if formulario.is_valid():
        formulario.save()
        return redirect("PROVEEDOR")
    else:
        print("Error en el formulario")
        print(formulario.errors)
    return render(request,"proveedores/añadirProveedor.html",{"formulario":formulario})

@login_required(login_url='LOGIN')
def generar_pdf_proveedor(request):
    proveedorr = proveedor.objects.all()
    template = get_template("proveedores/reporte_proveedores.html")

    context = {
        'proveedores': proveedorr,
        'fecha': datetime.now(),
        'reporte': True  # 👈 ESTA LÍNEA es la clave
    }
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment;filename = "reporte_proveedores.pdf"'
    pisa_status=pisa.CreatePDF(html,dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar PDF', status = 500)
    return response

@login_required(login_url='LOGIN')
def vista_previa_proveedor(request):
    proveedorr = proveedor.objects.all()
    return render(request, 'proveedores/reporte_proveedores.html',{'proveedores':proveedorr,'fecha': datetime.now(),"reporte": True})

#INICIO DE SESION
def loginP(request):
    if request.method =='POST':
        usuario = request.POST ['usuario']
        clave = request.POST ['clave']
        user = authenticate (request, username = usuario, password = clave)
        if user is not None:
            login(request,user)
            return redirect("PRODUCTOS")
        else:
            #messages.error(request,"Usuario o contraseña incorrecta")
            pass

        try:
            persona = Empleado.objects.get(nombre=usuario, password=clave)
            # Guardamos sesión manualmente
            request.session['persona_id'] = persona.id
            request.session['persona_nombre'] = persona.nombre
            return redirect("PRINCIPAL")
        except Empleado.DoesNotExist:
            messages.error(request, "\nUsuario o contraseña incorrecta")
    
    return render(request,"administracion/login.html")

def logoutP(request):
    logout(request)
    return redirect('PRINCIPAL')


#REGISTROS DE VENTAS 
def ventas(request):
    if request.method == 'GET':
        productoss = productos.objects.all()
        clientes_list = clientes.objects.all()
        empleados_list = Empleado.objects.all()
        fecha_actual = timezone.now().date()

        return render(request, 'ventas/venta4.html', {
            'productos': productoss,
            'clientes': clientes_list,
            'empleados': empleados_list,
            'fecha_actual': fecha_actual,
        })

    elif request.method == 'POST':
        try:
            cliente_id = request.POST.get('cliente_id')
            empleado_id = request.POST.get('empleado_id')
            fecha = request.POST.get('fecha')
            detalle_json = request.POST.get('detalle_json')

            cliente = get_object_or_404(clientes, id=cliente_id)
            empleado_instancia = get_object_or_404(Empleado, id=empleado_id)

            venta_instancia = venta.objects.create(
                cliente_id=cliente,
                empleado_id=empleado_instancia,
                fecha=fecha
            )

            # Convertir el JSON del carrito a lista de productos
            detalle_data = json.loads(detalle_json)

            if not detalle_data:
                messages.error(request, "No se ha registrado ningún producto en la venta.")
                venta_instancia.delete()
                return redirect('VENTAS')
            
            for item in detalle_data:
                prod = get_object_or_404(productos, id=item['id'])
                cantidad = int(item['cantidad'])
                precio = float(item['precio'])

                # Validar stock suficiente
                if prod.cantidad < cantidad:
                    messages.error(request, f"Stock insuficiente para {prod.descripcion}")
                    venta_instancia.delete()
                    return redirect('VENTAS')

                # Crear detalle
                detalle_venta.objects.create(
                    id_venta=venta_instancia,
                    id_prod=prod,
                    cantidad=cantidad,
                    precio=precio,
                    total=cantidad * precio
                )

                # Reducir stock y guardar
                print(f"🛒 Vendiendo {cantidad} de {prod.descripcion} (antes: {prod.cantidad})")
                prod.cantidad -= cantidad
                prod.save()
                
            #messages.success(request, "Venta registrada exitosamente.")
            #return redirect('ventas')  # Redirigir a la página de ventas
            return redirect('venta_exitosa', venta_id=venta_instancia.id)

        except Exception as e:
            messages.error(request, f"Error al procesar la venta: {e}")
            return redirect('VENTAS')

def ver_venta_exitosa(request,venta_id):
    venta_instancia = get_object_or_404(venta, id=venta_id)
    return render(request, 'ventas/venta_exitosa.html', {'venta_id': venta_id})

#GENERACION DE REPORTE DE VENTAS
def generar_pdf_venta(request, venta_id):
    venta_instancia = get_object_or_404(venta.objects.select_related('cliente_id', 'empleado_id'), id=venta_id)
    detalles = detalle_venta.objects.filter(id_venta=venta_instancia)
    total = sum(d.total for d in detalles)
    template = get_template('ventas/venta_pdf.html')
    context = {
        'venta': venta_instancia,
        'detalles': detalles,
        'total': total,
        'reporte': True 
    }
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=\"venta_{venta_id}.pdf\"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    return response

def listado_ventas(request):
    ventas = venta.objects.prefetch_related('detalles__id_prod').select_related('cliente_id', 'empleado_id').all()
    for v in ventas:
        v.total_venta = sum(d.total for d in v.detalles.all())
    total_general = sum(v.total_venta for v in ventas)
    return render(request, 'ventas/listado.html', {'ventas': ventas, 'total_general': total_general})

#VISION ARTIFICIAL
def camara(request):
    return render(request, "vision_artificial/camara.html")

def camara_red(request):
    return render(request, "vision_artificial/camara_red.html")

def consultafirebase(request):
    vision = get_config().get("vision", False)
    return render(request, "vision_artificial/consulta_firebase.html", {"vision": vision})

def toggle_vision(request):
    if request.method == "POST":
        activar_vision()  # Cambia False → True
    return redirect("consultafirebase")

#ADMINISTRADOR DE TAREAS
def principal_tecnica(request):
    return render(request, "trabajos/pagina_tecnica.html")


def trabajos_tecnica(request):

    empleados = Empleado.objects.all()
    clientess = clientes.objects.all()

    if request.method == "POST":

        proyectos_data = request.POST.get("proyectos_data")
        empleado_id = request.POST.get("empleado")
        cliente_id = request.POST.get("cliente")

        if proyectos_data and empleado_id and cliente_id:
            data = json.loads(proyectos_data)

            # 🔹 CREAR SOLO UN PROYECTO
            proyecto = proyectos.objects.create(
                empleado_id=empleado_id,
                cliente_id=cliente_id
            )

            # 🔹 CREAR MUCHOS DETALLES
            for p in data:
                detalle_proyecto.objects.create(
                    id_proyecto=proyecto,
                    categoria=p["categoria"],
                    especificacion=p["especificacion"],
                    fecha_coordinacion=p["fecha_coordinacion"],
                    fecha_entrega=p["fecha_entrega"]
                )

        return redirect("TRABAJOS_TECNICA")

    context = {
        "empleados": empleados,
        "clientes": clientess,
    }

    return render(request, "trabajos/trabajos_tecnica.html", context)
