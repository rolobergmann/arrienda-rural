from django.db import models
from django.contrib import admin
# Create your models here.
class Direccion(models.Model):
    calle = models.CharField(max_length=50,null=False)
    numero = models.CharField(max_length=10,null=False)
    depto = models.CharField(max_length=50)
    comuna = models.CharField(max_length=50,null=False)
    ciudad = models.CharField(max_length=50, null=False)
    region = models.CharField(max_length=50, null=False)
 
    
    def __str__(self):
        return self.calle + ' ' + self.numero
    
class DireccionAdmin(admin.ModelAdmin):
    list_display = ('calle', 'numero', 'depto', 'comuna', 'ciudad', 'region')
    filter_fields = ('region','ciudad','comuna')
class Usuario(models.Model):
    rut = models.CharField(max_length=9, unique=True,primary_key=True, null=False, blank=False)
    Nombre_1 = models.CharField(max_length=50)
    Nombre_2 = models.CharField(max_length=50)
    Apellido_1 = models.CharField(max_length=50)
    Apellido_2 = models.CharField(max_length=50)
    email = models.EmailField()
    telefono = models.CharField(max_length=9)
    tipo_de_usuario = models.CharField(max_length=20)
    direccion = models.OneToOneField(Direccion, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'usuario'
        
    def __str__(self):
        return self.rut + ' ' + self.Nombre_1 + ' ' + self.Apellido_1

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('rut', 'Nombre_1', 'Nombre_2', 'Apellido_1', 'Apellido_2', 'email', 'telefono', 'tipo_de_usuario', 'direccion')
    search_fields = ('rut','Apellido_1')
    filter_fields = ('tipo_de_usuario')

    def get_direccion(self, obj):
        if obj.direccion:
            address_template = "{calle} {numero}, {depto}. {comuna}, {ciudad}, Región de {region}"
            return address_template.format(**obj.direccion.__dict__) 
        return '-'


class Inmueble(models.Model):
    nombre = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)
    m2_construidos = models.IntegerField(null=False)
    m2_totales = models.IntegerField(null=False)
    estacionamientos = models.IntegerField(null=False)
    cantidad_habitaciones= models.IntegerField(null=False)
    cantidad_banos = models.IntegerField(null=False)
    tipo_de_inmueble = models.CharField(max_length=50, null=False)
    precio_arriendo = models.IntegerField(null=False)
    direccion = models.OneToOneField(Direccion, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'inmueble'
        
    def __str__(self):
        return self.nombre

class InmuebleAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'description', 'm2_construidos', 'm2_totales', 'estacionamientos', 'cantidad_habitaciones', 'cantidad_banos', 'tipo_de_inmueble', 'precio_arriendo')
    search_fields = ('nombre','tipo_de_inmueble')
    filter_fields = ('tipo_de_inmueble')

