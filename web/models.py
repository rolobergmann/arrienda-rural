from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager

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
    nombre_1 = models.CharField(max_length=50)
    nombre_2 = models.CharField(max_length=50)
    apellido_1 = models.CharField(max_length=50)
    apellido_2 = models.CharField(max_length=50)
    email = models.EmailField()
    telefono = models.CharField(max_length=9)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_ELECCIONES,default='Arrendatario')
    direccion = models.OneToOneField(Direccion, on_delete=models.DO_NOTHING, null=True, blank=True)
    password = models.CharField(max_length=50, null=False, blank=False)

    groups = models.ManyToManyField(
        Group,
        verbose_name="Grupos",
        blank=True,
        help_text="Los grupos a los que pertenece este usuario. Un usuario obtendrá todos los permisos otorgados a cada uno de los grupos en los que se encuentra.",
        related_name="usuario_groups"  # Nombre personalizado para la relación inversa
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="Permisos del usuario",
        blank=True,
        help_text="Permisos específicos para este usuario.",
        related_name="usuario_permissions"  # Nombre personalizado para la relación inversa
    )
    def __str__(self):
        return self.nombre_1 + ' ' + self.apellido_1

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


class ContactForm(models.Model) :
    contact_form_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=64)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.customer_name + ' ' + self.date_sent.strftime("%d/%m/%Y")