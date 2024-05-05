from django.contrib import admin
from .models import *

# Register your models here.
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('rut', 'Nombre_1', 'Nombre_2', 'Apellido_1', 'Apellido_2', 'email', 'telefono', 'tipo_usuario', 'direccion')
    search_fields = ('rut','Apellido_1')
    filter_fields = ('tipo_usuario')

    def get_direccion(self, obj):
        if obj.direccion:
            address_template = "{calle} {numero}, {depto}. {comuna}, {ciudad}, Región de {region}"
            return address_template.format(**obj.direccion.__dict__) 
        return '-'
admin.site.register(Usuario,UsuarioAdmin)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ('calle', 'numero', 'depto', 'comuna', 'ciudad', 'region')
    filter_fields = ('region','ciudad','comuna')
admin.site.register(Direccion,DireccionAdmin)
class InmuebleAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'description', 'm2_construidos', 'm2_totales', 'estacionamientos', 'cantidad_habitaciones', 'cantidad_banos', 'tipo_de_inmueble', 'precio_arriendo')
    search_fields = ('nombre','tipo_de_inmueble')
    filter_fields = ('tipo_de_inmueble')
admin.site.register(Inmueble,InmuebleAdmin)