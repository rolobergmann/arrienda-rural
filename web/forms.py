from django import forms
from .models import ContactForm, ExtendUsuario, Inmueble, ComunasChile,RegionesChile, Direccion,Imagen
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.forms.widgets import ClearableFileInput

# Create the form class.

class ContactFormModelForm(forms.ModelForm) :
    class Meta :
        model = ContactForm
        fields = ['customer_email', 'customer_name', 'message']
        labels = {'customer_email' : 'Correo', 'customer_name' : 'Nombre', 'message' : 'Mensaje', 'rut' : 'Rut'}
        widgets = {'customer_email' : forms.EmailInput(attrs={'placeholder': 'Correo'}),
        'customer_name' : forms.TextInput(attrs={'placeholder': 'Tu nombre'}),
        'message' : forms.Textarea(attrs={'placeholder': 'Mensaje'})
        }


class RegistroForm(UserCreationForm):
    # Add your ExtendUsuario fields here
    rut = forms.CharField(label="RUT", max_length=50)
    email = forms.EmailField(label="Correo Electrónico")
    nombre_1 = forms.CharField(label="Primer Nombre", max_length=50)
    nombre_2 = forms.CharField(label="Segundo Nombre", max_length=50, required=False)  # Optional
    apellido_1 = forms.CharField(label="Primer Apellido", max_length=50)
    apellido_2 = forms.CharField(label="Segundo Apellido", max_length=50, required=False)  # Optional
    telefono = forms.CharField(label="Teléfono", max_length=15)
    tipo_usuario = forms.ChoiceField(label="Tipo de Usuario", choices=ExtendUsuario.TIPO_USUARIO_ELECCIONES)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('rut', 'email','nombre_1', 'nombre_2', 'apellido_1', 'apellido_2', 'telefono', 'tipo_usuario')

#ExtendUsuarioFormSet = inlineformset_factory(User, ExtendUsuario, fields=('rut', 'nombre_1', 'nombre_2', 'apellido_1', 'apellido_2', 'telefono', 'tipo_usuario'), can_delete=False)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = ExtendUsuario
        fields = ['nombre_1', 'nombre_2', 'apellido_1', 'apellido_2', 'telefono'] 
class InmuebleUpdateForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = ['nombre', 'description', 'm2_construidos', 'm2_totales', 'estacionamientos', 'cantidad_habitaciones', 'cantidad_banos', 'tipo_de_inmueble', 'precio_arriendo', 'estado','destacado', 'disponible']
        labels = {'cantidad_banos':'Cantidad de baños'}

class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class InmuebleCreationForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = ['nombre', 'description', 'm2_construidos', 'm2_totales', 'estacionamientos', 'cantidad_habitaciones', 'cantidad_banos', 'tipo_de_inmueble', 'precio_arriendo', 'estado', 'destacado', 'disponible']

class AddPhotoForm(forms.ModelForm):
    imagenes = MultipleFileField()

    class Meta:
        model = Inmueble
        fields = ['nombre', 'description', 'm2_construidos', 'm2_totales', 'estacionamientos', 'cantidad_habitaciones', 'cantidad_banos', 'tipo_de_inmueble', 'precio_arriendo', 'estado', 'destacado', 'disponible']

    def save(self, commit=True):
        result = super().save(commit=commit)
        if commit:
            for image in self.cleaned_data['imagenes']:
                Imagen(inmueble=result, imagen=image).save()
        return result
class DireccionForm(forms.ModelForm):
    region = forms.ModelChoiceField(queryset=RegionesChile.objects.all(), required=True)
    comuna = forms.ModelChoiceField(queryset=ComunasChile.objects.none(), required=True)
    
    class Meta:
        model = Direccion
        fields = ['calle', 'numero', 'depto', 'region', 'comuna']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['comuna'].queryset = ComunasChile.objects.filter(region_id=region_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['comuna'].queryset = self.instance.region.comunaschile_set.order_by('nombre')