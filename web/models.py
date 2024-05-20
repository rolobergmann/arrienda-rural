from django.db import models
import uuid
from django.contrib.auth.models import User
class RegionesChile(models.Model):  
    nombre = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.nombre


class ComunasChile(models.Model):  
    nombre = models.CharField(max_length=50, null=False)
    region = models.ForeignKey(RegionesChile, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.nombre
class Direccion(models.Model):
    calle = models.CharField(max_length=50, null=False)
    numero = models.CharField(max_length=10, null=True)
    depto = models.CharField(max_length=50, null=True)
    comuna = models.ForeignKey(ComunasChile, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.calle} {self.numero}, {self.comuna}"
class Inmueble(models.Model):
    TIPO_INMUEBLE_ELECCIONES = (
        ('casa', 'Casa'), 
        ('departamento', 'Departamento'),
        ('parcela', 'Parcela')
    )
    nombre = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)
    m2_construidos = models.IntegerField(null=False)
    m2_totales = models.IntegerField(null=False)
    estacionamientos = models.IntegerField(null=False)
    cantidad_habitaciones = models.IntegerField(null=False)
    cantidad_banos = models.IntegerField(null=False)
    tipo_de_inmueble = models.CharField(max_length=20, choices=TIPO_INMUEBLE_ELECCIONES, default='Casa')
    precio_arriendo = models.IntegerField(null=False)
    estado = models.BooleanField(default=False, choices=(
        (True, 'Disponible'),
        (False, 'No disponible')
    ))
    destacado = models.BooleanField(default=False)
    disponible = models.BooleanField(default=True)
    direccion_id = models.OneToOneField('Direccion', on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.tipo_de_inmueble + ' ' + self.nombre + ' ' + str(self.precio_arriendo)



class ContactForm(models.Model) :
    contact_form_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=64)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.customer_name + ' ' + self.date_sent.strftime("%d/%m/%Y")

class ExtendUsuario(models.Model):
    TIPO_USUARIO_ELECCIONES = (
        ('arrendador', 'Arrendador'), 
        ('arrendatario', 'Arrendatario')
    )
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    rut = models.CharField(max_length=10, unique=True, primary_key=True, null=False, blank=False, verbose_name="RUT")
    nombre_1 = models.CharField(max_length=50, verbose_name="Nombre_1")
    nombre_2 = models.CharField(max_length=50, verbose_name="Nombre_2")
    apellido_1 = models.CharField(max_length=50, verbose_name="Apellido_1")
    apellido_2 = models.CharField(max_length=50, verbose_name="Apellido_2")
    telefono = models.CharField(max_length=15, verbose_name="Telefono")
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_ELECCIONES, default='Arrendatario', verbose_name="Tipo_usuario")
    direccion = models.OneToOneField(Direccion, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="Direccion")
    inmuebles_arrendados = models.ManyToManyField(Inmueble, blank=True, verbose_name="Inmuebles Arrendados", related_name="arrendatarios")
    
    def __str__(self):
        return f"{self.usuario.username} - Perfil"

class Imagen(models.Model):
    inmueble = models.ForeignKey(Inmueble, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='arrienda_rural/front/assets/media/inmuebles')

    def __str__(self):
        return f"Imagen de {self.inmueble.nombre}"