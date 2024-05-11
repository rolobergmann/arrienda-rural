from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils import timezone

from web.forms import ContactFormModelForm,RegistroForm
from web.models import ContactForm


def index(request):
    return render(request, "index.html")


def exito(request):
    return render(request, "exito.html")

def loggedout(request):
    return render(request, "registration/logged_out.html")


# Create your views here.


def contacto(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ContactFormModelForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form. cleaned_data as required
            # ...
            # redirect to a new URL:
            contact_form = ContactForm.objects.create(**form.cleaned_data)
            return HttpResponseRedirect("/exito")

        # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactFormModelForm()

    return render(request, "contactus.html", {"form": form})


def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            nuevo_usuario = form.save()
            # Autentificar al usuario recién creado
            usuario_autenticado = authenticate(username=nuevo_usuario.username, password=form.cleaned_data['password1'])
            if usuario_autenticado:
                login(request, usuario_autenticado)
                return redirect("/")
            else:
                return render(request, "registration/register.html", {"form": form, "mensaje_error": "Error al iniciar sesión"})
    else:
        form = RegistroForm()
    return render(request, "registration/register.html", {"form": form})


def exit(request):
    logout(request)
    return redirect("loggedout")
