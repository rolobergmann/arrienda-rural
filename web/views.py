from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import Template, Context, loader
from web.models import ContactForm
from web.forms import ContactFormModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
""" from web.forms import UserForm """

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