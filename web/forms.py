from django import forms
from django.forms import ModelForm
from .models import ContactForm, ExtendUsuario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory


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
    rut = forms.CharField(label="RUT", max_length=10)
    nombre_1 = forms.CharField(label="Primer Nombre", max_length=50)
    nombre_2 = forms.CharField(label="Segundo Nombre", max_length=50, required=False)  # Optional
    apellido_1 = forms.CharField(label="Primer Apellido", max_length=50)
    apellido_2 = forms.CharField(label="Segundo Apellido", max_length=50, required=False)  # Optional
    telefono = forms.CharField(label="Teléfono", max_length=15)
    tipo_usuario = forms.ChoiceField(label="Tipo de Usuario", choices=ExtendUsuario.TIPO_USUARIO_ELECCIONES)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('rut', 'nombre_1', 'nombre_2', 'apellido_1', 'apellido_2', 'telefono', 'tipo_usuario')

#ExtendUsuarioFormSet = inlineformset_factory(User, ExtendUsuario, fields=('rut', 'nombre_1', 'nombre_2', 'apellido_1', 'apellido_2', 'telefono', 'tipo_usuario'), can_delete=False)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = ExtendUsuario
        fields = ['nombre_1', 'nombre_2', 'apellido_1', 'apellido_2', 'telefono'] # Choose the fields you want users to edit