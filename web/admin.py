from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Usuario,UsuarioAdmin)
admin.site.register(Direccion,DireccionAdmin)
admin.site.register(Inmueble,InmuebleAdmin)