from django.db import models
# Create your models here.
class Direccion(models.Model):
    calle = models.CharField(max_length=50,null=False)
    numero = models.CharField(max_length=10,null=False)
    depto = models.CharField(max_length=50)
    comuna = models.CharField(max_length=50,null=False)
    ciudad = models.CharField(max_length=50, null=False)
    region = models.CharField(max_length=50, null=False)

        
    def __str__(self):
        return self.calle + ' ' + self.numero + ', ' + self.comuna
    

class Usuario(models.Model):
    TIPO_USUARIO_ELECCIONES = (
        ('arrendador', 'Arrendador'), 
        ('arrendatario', 'Arrendatario')
    )
    rut = models.CharField(max_length=10, unique=True,primary_key=True, null=False, blank=False)
    Nombre_1 = models.CharField(max_length=50)
    Nombre_2 = models.CharField(max_length=50)
    Apellido_1 = models.CharField(max_length=50)
    Apellido_2 = models.CharField(max_length=50)
    email = models.EmailField()
    telefono = models.CharField(max_length=9)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_ELECCIONES,default='Arrendatario')
    direccion = models.OneToOneField(Direccion, on_delete=models.DO_NOTHING, null=True, blank=True)
        
    def __str__(self):
        return self.Nombre_1 + ' ' + self.Apellido_1




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
        
    def __str__(self):
        return self.tipo_de_inmueble + ' ' + self.nombre + ' ' + str(self.precio_arriendo)




