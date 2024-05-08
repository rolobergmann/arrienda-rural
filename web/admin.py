from django.contrib import admin
from .models import *
from .models import ContactForm
import datetime

class DateSentFilter(admin.SimpleListFilter):
    title = 'Enviados en'
    parameter_name = 'date_sent'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Hoy'),
            ('past_7_days', 'Semana pasada'),
            ('this_month', 'Este mes'),
        )

    def queryset(self, request, queryset):
        today = datetime.date.today()
        if self.value() == 'today':
            return queryset.filter(date_sent__date=today)
        if self.value() == 'past_7_days':
            one_week_ago = today - datetime.timedelta(days=7)
            return queryset.filter(date_sent__gte=one_week_ago, date_sent__lte=today)
        if self.value() == 'this_month':
            return queryset.filter(date_sent__year=today.year, date_sent__month=today.month)

# Register your models here.
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre_1', 'nombre_2', 'apellido_1', 'apellido_2',
                    'email', 'telefono', 'tipo_usuario', 'direccion')
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

class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('customer_name','customer_email','message','date_sent')
    search_fields =('rut','customer_email')
    list_filter = (DateSentFilter, 'customer_email')
admin.site.register(ContactForm,ContactFormAdmin)