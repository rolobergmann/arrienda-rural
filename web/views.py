from django.contrib.auth import login, authenticate, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView

from web.forms import ContactFormModelForm,RegistroForm, UserUpdateForm
from web.models import ContactForm, Inmueble, RegionesChile, ComunasChile, ExtendUsuario
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  
from django.contrib.auth.views import redirect_to_login
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied

class ArrendarListView(ListView):
    model = Inmueble
    template_name = 'inmueble_list.html'
    context_object_name = 'inmuebles'

    def get_queryset(self):
        queryset = Inmueble.objects.all()

        region_id = self.request.GET.get('region')
        if region_id:
            queryset = queryset.filter(direccion__comuna__region_id=region_id)

        comuna_id = self.request.GET.get('comuna')
        if comuna_id:
            queryset = queryset.filter(direccion__comuna_id=comuna_id)

        tipo_de_inmueble = self.request.GET.get('tipo_de_inmueble')
        if tipo_de_inmueble:
            queryset = queryset.filter(tipo_de_inmueble=tipo_de_inmueble)
        
        imagenes = self.request.GET.get('imagenes')
        if imagenes == 'Not Null':
            queryset = queryset.exclude(imagenes__isnull=True)
        elif imagenes == 'Null':
            queryset = queryset.filter(imagenes__isnull=True)


        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regiones'] = RegionesChile.objects.all()  # Add regions for the filter
        context['tipos_de_inmueble'] = Inmueble.TIPO_INMUEBLE_ELECCIONES  # Add tipos de inmueble
        context['selected_imagenes'] = self.request.GET.get('imagenes', '')
        return context


def index(request):
    inmuebles_destacados = Inmueble.objects.filter(destacado=True, disponible=True)
    return render(request, 'index.html', {'inmuebles_destacados': inmuebles_destacados}) 

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

class ArrendatarioAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'arrendatario_account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = ExtendUsuario.objects.get(usuario=self.request.user)  # Assuming ExtendUsuario is your extended user model
        # Add other relevant data for arrendatarios
        return context

class ArrendadorAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'arrendador_account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = ExtendUsuario.objects.get(usuario=self.request.user)  
        # Add other relevant data for arrendadores
        return context
@login_required 
def user_redirect_view(request):
    if not request.user.is_authenticated:
        return redirect_to_login(request.get_full_path(), login_url='/accounts/login/', redirect_field_name=REDIRECT_FIELD_NAME)

    try:
        user_profile = ExtendUsuario.objects.get(usuario=request.user)
        if user_profile.tipo_usuario == 'arrendador':
            return redirect('arrendador_account')  
        elif user_profile.tipo_usuario == 'arrendatario':
            return redirect('arrendatario_account')
        else:
            return redirect('index')
    except ExtendUsuario.DoesNotExist:
        return redirect('index')
    
class ArrendatarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ExtendUsuario
    form_class = UserUpdateForm
    template_name = 'arrendatario_update.html'

    def test_func(self):
        profile = self.get_object()
        if profile.usuario == self.request.user and profile.tipo_usuario == 'arrendatario':
            return True
        else:
            raise PermissionDenied("No tienes permiso para editar este perfil.")
    
    def form_valid(self, form):
        messages.success(self.request, '¡Tus datos han sido guardados exitosamente!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('arrendatario_account')
    

class ArrendadorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ExtendUsuario
    form_class = UserUpdateForm
    template_name = 'arrendador_update.html'

    def test_func(self):
        profile = self.get_object()
        if profile.usuario == self.request.user and profile.tipo_usuario == 'arrendador':
            return True
        else:
            raise PermissionDenied("No tienes permiso para editar este perfil.")
    
    def form_valid(self, form):
        messages.success(self.request, '¡Tus datos de arrendador han sido guardados exitosamente!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('arrendador_account')
        
def inmueble_view(request, pk):
    inmueble = get_object_or_404(Inmueble, pk=pk)
    return render(request, 'inmueble_view.html', {'inmueble': inmueble})