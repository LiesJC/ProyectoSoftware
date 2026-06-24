from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(productos)
admin.site.register(proveedor)
admin.site.register(Empleado)
admin.site.register(clientes)
admin.site.register(detalle_venta)
admin.site.register(venta)
#admin.site.register(detalle_compra)
#admin.site.register(compra)
