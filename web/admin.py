from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .models import ContactForm, ExtendUsuario, User,Imagen
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

class DireccionAdmin(admin.ModelAdmin):
    list_display = ('calle', 'numero', 'depto', 'get_comuna_nombre', 'get_region_nombre')
    
    def get_comuna_nombre(self, obj):
        return obj.comuna.nombre if obj.comuna else "-"

    def get_region_nombre(self, obj):
        return obj.comuna.region.nombre if obj.comuna else "-"

    get_comuna_nombre.short_description = 'Comuna'
    get_region_nombre.short_description = 'Region'
admin.site.register(Direccion, DireccionAdmin)

class ImagenInline(admin.TabularInline):
    model = Imagen
    extra = 2  # Número de imágenes adicionales para agregar por defecto
class InmuebleAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'description', 'm2_construidos', 'm2_totales', 'estacionamientos', 'cantidad_habitaciones', 'cantidad_banos', 'tipo_de_inmueble', 'precio_arriendo')
    search_fields = ('nombre','tipo_de_inmueble')
    list_filter = ('tipo_de_inmueble','cantidad_habitaciones','cantidad_banos','estacionamientos')
    
    inlines = [ImagenInline]
    
admin.site.register(Inmueble,InmuebleAdmin)

class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('customer_name','customer_email','message','date_sent')
    search_fields =('rut','customer_email')
    list_filter = (DateSentFilter, 'customer_email')
admin.site.register(ContactForm,ContactFormAdmin)

class ExtendUsuarioAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre_1', 'apellido_1', 'tipo_usuario', 'telefono')  # Fields to display in the admin list view
    list_filter = ('tipo_usuario',)  # Fields to add filters on the admin list view
    search_fields = ('username', 'rut', 'nombre_1', 'apellido_1')  # Fields to search in the admin list view

class ExtendUsuarioInline(admin.StackedInline): 
    model = ExtendUsuario 
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (ExtendUsuarioInline,)

admin.site.unregister(User)  # Unregister the default UserAdmin
admin.site.register(User, CustomUserAdmin)  # Register your custom UserAdmin

""" class ImagenAdmin(admin.ModelAdmin):
    list_display = ('inmueble', 'imagen')

admin.site.register(Imagen, ImagenAdmin) """



