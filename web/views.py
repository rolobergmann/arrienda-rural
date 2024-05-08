from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import Template, Context, loader
from web.models import ContactForm
from web.forms import ContactFormModelForm, UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.utils import timezone

def index(request):
    return render(request, "index.html")

def exito(request):
    return render(request, "exito.html")
# Create your views here.

def contacto(request) :
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactFormModelForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form. cleaned_data as required
            # ...
            # redirect to a new URL:
            contact_form = ContactForm.objects.create(**form.cleaned_data)
            return HttpResponseRedirect('/exito')

        # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactFormModelForm()

    return render(request, 'contactus.html', {'form': form})

from django.contrib.auth.hashers import make_password  # Importa la función de hashing

def registro(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.date_joined = timezone.now()  # Establece la fecha y hora actual
            user.save()
            return redirect('/')
    else:
        form = UserForm()
    return render(request, "registration/register.html", {'form': form})


""" def logout(request):
    logout(request)
    return redirect('/loggedout') """