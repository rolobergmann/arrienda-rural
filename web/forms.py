from django import forms
from django.forms import ModelForm
from .models import ContactForm, Usuario
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create the form class.

class ContactFormModelForm(forms.ModelForm) :
    class Meta :
        model = ContactForm
        fields = ['customer_email', 'customer_name', 'message', 'rut']
        labels = {'customer_email' : 'Correo', 'customer_name' : 'Nombre', 'message' : 'Mensaje', 'rut' : 'Rut'}
        widgets = {'customer_email' : forms.EmailInput(attrs={'placeholder': 'Correo'}),
        'customer_name' : forms.TextInput(attrs={'placeholder': 'Tu nombre'}),
        'message' : forms.Textarea(attrs={'placeholder': 'Mensaje'}),
        'rut': forms.TextInput(attrs={'placeholder': 'Ej: 12345678-9 (opcional)', 'length': '12','null': True, 'blank': True})
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('username',
            'rut', 'nombre_1', 'nombre_2', 'apellido_1', 'apellido_2',
            'email', 'telefono', 'tipo_usuario','password'
        )
        widgets = {'username': forms.TextInput,
            'rut': forms.TextInput, 'nombre_1': forms.TextInput, 'nombre_2': forms.TextInput,
            'apellido_1': forms.TextInput, 'apellido_2': forms.TextInput,
            'email': forms.EmailInput, 'telefono': forms.TextInput,
            'tipo_usuario': forms.Select, 'password': forms.PasswordInput
        }

    # Si deseas, puedes añadir validación adicional, por ejemplo, para el campo rut:
    def clean_rut(self):
        rut = self.cleaned_data['rut']
        # Implementar lógica de validación de RUT (dígito verificador, etc.)
        return rut