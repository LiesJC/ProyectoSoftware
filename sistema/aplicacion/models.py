from django.db import models
from django.utils import timezone
# Create your models here.

class productos(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50,default="",verbose_name="Descripcion")
    marca = models.CharField(max_length=20,default="",verbose_name="Marca")
    procedencia = models.CharField(max_length=20, default="",verbose_name="Procedencia")
    cantidad = models.IntegerField(default=0,verbose_name="Cantidad reservada")
    precio = models.DecimalField(max_digits=10,decimal_places=2,default=0.00, verbose_name="Precio unitario")
    stockmaximo = models.IntegerField(default=0,verbose_name="Stock en tienda")
    categoria = models.CharField(max_length=20,default="",verbose_name="Categoria")
    imagen = models.ImageField(upload_to='imagenes',default="imagenes/default.png",verbose_name="Imagen")
    def __str__(self):
        return self.descripcion
    
class proveedor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50,default="",verbose_name="Nombre")
    telefono = models.IntegerField(default=0,verbose_name="Telefono")
    direccion = models.TextField(max_length=50,default="",verbose_name="Dirección")
    correo = models.EmailField(max_length=50,default="",verbose_name="Correo")
    pagina = models.CharField(max_length=50,default="",verbose_name="PaginaWeb")  
    imagen = models.ImageField(upload_to='imagenes',default="imagenes/default.png",verbose_name="Imagen")
    def __str__(self):
        return self.nombre  

class Empleado(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50,default="",verbose_name="Nombre")
    a_paterno = models.CharField(max_length=50,default="",verbose_name="Apellido Paterno")
    a_materno = models.CharField(max_length=50,default="",verbose_name="Apellido Materno")
    telefono = models.IntegerField(default=0,verbose_name="Telefono")
    direccion = models.TextField(max_length=50,default="",verbose_name="Dirección")
    correo = models.EmailField(max_length=50,default="",verbose_name="Correo")
    profesion = models.CharField(max_length=50,default="",verbose_name="Profesion")
    nacimiento = models.DateField(blank=True,null=True,verbose_name="Fecha de nacimiento")
    ingreso = models.DateField(blank=True, null=True ,verbose_name="Fecha de ingreso")
    estado_civil = models.CharField(max_length=50,default="",verbose_name="Estado civil")
    cargo =  models.CharField(max_length=50,default="",verbose_name="Cargo")
    sueldo = models.IntegerField(default=0,verbose_name="Sueldo")
    password = models.CharField(max_length=50,default="",verbose_name="Contraseña")

    def __str__(self):
        return self.nombre

class clientes(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50,default="",verbose_name="Nombre")
    a_paterno = models.CharField(max_length=50,default="",verbose_name="Apellido_P")
    a_materno = models.CharField(max_length=50,default="",verbose_name="Apellido_M")
    nit = models.CharField(max_length=20,default="",verbose_name="Nit")
    telefono = models.IntegerField(default=0,verbose_name="Telefono")
    correo = models.EmailField(max_length=50,default="",verbose_name="Correo")
    def __str__(self):
        return self.nombre

class Compra(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Nro. Compra")
    fecha = models.DateField(default=timezone.now, verbose_name="Fecha de Compra")

    proveedor_id = models.ForeignKey(
        'proveedor',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Proveedor"
    )

    empleado_id = models.ForeignKey(
        'Empleado',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Empleado Responsable"
    )

    def __str__(self):
        return f"Compra #{self.id} -Proveedor: {self.proveedor_id.nombre if self.proveedor_id else 'N/A'} - Empleado: {self.empleado_id.nombre if self.empleado_id else 'N/A'}"

class detalle_compra(models.Model):
    id_compra = models.ForeignKey(
        Compra,
        on_delete=models.CASCADE,
        related_name='detalles',  # ✅ nombre de relación inversa
        verbose_name="Compra"
    )
    id_prod = models.ForeignKey(
        productos,
        on_delete=models.CASCADE,
        verbose_name="Producto"
    )
    cantidad = models.IntegerField(default=1, verbose_name="Cantidad")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total", editable=False)

    def save(self, *args, **kwargs):
        self.total = self.cantidad * self.precio
        super().save(*args, **kwargs)

class venta(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Nro. Venta")
    fecha = models.DateField(default=timezone.now, verbose_name="Fecha de Venta")

    empleado_id = models.ForeignKey(
        'Empleado',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Empleado Responsable"
    )

    cliente_id = models.ForeignKey(
        'clientes',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Cliente"
    )

    def __str__(self):
        return f"venta #{self.nro_venta} - Cliente: {self.cliente_id.nombre if self.cliente_id else 'N/A'} - Empleado: {self.empleado_id.nombre if self.empleado_id else 'N/A'}"

class detalle_venta(models.Model):
    id_venta = models.ForeignKey(
        venta,
        on_delete=models.CASCADE,
        related_name='detalles',  # ✅ nombre de relación inversa
        verbose_name="Venta"
    )
    id_prod = models.ForeignKey(
        productos,
        on_delete=models.CASCADE,
        verbose_name="Producto"
    )
    cantidad = models.IntegerField(default=1, verbose_name="Cantidad")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total", editable=False)

    def save(self, *args, **kwargs):
        self.total = self.cantidad * self.precio
        super().save(*args,**kwargs)

class proyectos(models.Model):
    id = models.AutoField(primary_key=True)

    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        related_name="proyectos",
        verbose_name="Empleado"
    )

    cliente = models.ForeignKey(
        clientes,
        on_delete=models.CASCADE,
        related_name="proyectos",
        verbose_name="Cliente"
    )

    def __str__(self):
        return f"Proyecto #{self.id}"
    
class detalle_proyecto(models.Model):
    id_proyecto = models.ForeignKey(
        proyectos,
        on_delete=models.CASCADE,
        related_name="detalles",
        verbose_name="Proyecto"
    )

    categoria = models.CharField(max_length=100, verbose_name="Categoría")
    especificacion = models.TextField(max_length=100, verbose_name="Especificación")

    fecha_coordinacion = models.DateTimeField(
        verbose_name="Fecha de coordinación"
    )

    fecha_entrega = models.DateTimeField(
        verbose_name="Fecha de entrega"
    )

    def __str__(self):
        return f"Detalle del Proyecto #{self.id_proyecto.id}"

