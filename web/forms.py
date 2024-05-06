from django import forms
from django.forms import ModelForm
from .models import ContactForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create the form class.

class ContactFormModelForm(forms.ModelForm) :
    class Meta :
        model = ContactForm
        fields = ['customer_email', 'customer_name', 'message']
        labels = {'customer_email' : 'Correo', 'customer_name' : 'Nombre', 'message' : 'Mensaje'}
        widgets = {'customer_email' : forms.EmailInput(attrs={'placeholder': 'Correo'}), 'customer_name' : forms.TextInput(attrs={'placeholder': 'Tu nombre'}), 'message' : forms.Textarea(attrs={'placeholder': 'Mensaje'})}


""" class UserForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2') """