from django.contrib.auth import login, authenticate, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import InmuebleCreationForm, DireccionForm
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView

from web.forms import MultipleImageForm,ContactFormModelForm,RegistroForm, UserUpdateForm,InmuebleCreationForm,DireccionForm,InmuebleUpdateForm
from web.models import ContactForm, Inmueble, RegionesChile, ComunasChile, ExtendUsuario,Imagen
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  
from django.contrib.auth.views import redirect_to_login
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.generic.edit import UpdateView, FormView



class ArrendarListView(ListView):
    model = Inmueble
    template_name = 'inmueble_list.html'
    context_object_name = 'inmuebles'

    def get_queryset(self):
        queryset = Inmueble.objects.all()

        region_id = self.request.GET.get('region')
        if region_id:
            queryset = queryset.filter(direccion_id__comuna__region_id=region_id)

        comuna_id = self.request.GET.get('comuna')
        if comuna_id:
            queryset = queryset.filter(direccion_id__comuna_id=comuna_id)

        tipo_de_inmueble = self.request.GET.get('tipo_de_inmueble')
        if tipo_de_inmueble:
            queryset = queryset.filter(tipo_de_inmueble=tipo_de_inmueble)

        imagenes = self.request.GET.get('imagenes')
        if imagenes == 'Not Null':
            queryset = queryset.filter(imagenes__isnull=False).distinct()
        elif imagenes == 'Null':
            queryset = queryset.filter(imagenes__isnull=True).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regiones'] = RegionesChile.objects.all()  # Add regions for the filter
        context['tipos_de_inmueble'] = Inmueble.TIPO_INMUEBLE_ELECCIONES  # Add tipos de inmueble
        context['selected_imagenes'] = self.request.GET.get('imagenes', '')
        for inmueble in context['inmuebles']:
            inmueble.esta_arrendado = inmueble.estado == False
        return context




def index(request):
    inmuebles_destacados = Inmueble.objects.filter(destacado=True, disponible=True)
    return render(request, 'index.html', {'inmuebles_destacados': inmuebles_destacados}) 

def exito(request):
    return render(request, "exito.html")


def arrendar(request):
    return render(request, "arrendar.html")




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
        else:
            print(form.errors)


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
    return redirect("index")

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
        context['inmuebles_publicados'] = Inmueble.objects.filter(owner=self.request.user) # Obtiene los inmuebles publicados por el usuario actual
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
    imagenes = inmueble.imagenes.all()
    return render(request, 'inmueble_view.html', {'inmueble': inmueble, 'imagenes': imagenes})

def confirmar_arriendo(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    usuario_extendido = ExtendUsuario.objects.get(usuario=request.user)  # Obtener el perfil del usuario extendido

    if usuario_extendido.tipo_usuario == 'arrendatario':
        if usuario_extendido.inmuebles_arrendados.filter(id=inmueble_id).exists():
            messages.error(request, "Ya has arrendado este inmueble.")
        else:
            usuario_extendido.inmuebles_arrendados.add(inmueble)
            usuario_extendido.save()
            inmueble.estado = False #cambiar el estado del inmueble a no disponible
            inmueble.save()
            messages.success(request, "¡Has arrendado el inmueble exitosamente!")
    else:
        if usuario_extendido.inmuebles_arrendados.filter(id=inmueble_id).exists():
            messages.error(request, "Ya tienes este inmueble en tu lista de inmuebles arrendados")
        else:
            usuario_extendido.inmuebles_arrendados.add(inmueble)
            usuario_extendido.save()
            inmueble.estado = False #cambiar el estado del inmueble a no disponible
            inmueble.save()
            messages.success(request, "¡El inmueble se ha agregado a tu lista de inmuebles arrendados!")

    return redirect('vista_inmueble', pk=inmueble_id)


def cargar_comunas(request):
    region_id = request.GET.get('region_id')
    comunas = ComunasChile.objects.filter(region_id=region_id).order_by('nombre')
    return JsonResponse(list(comunas.values('id', 'nombre')), safe=False)

class InmuebleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Inmueble
    form_class = InmuebleUpdateForm
    template_name = 'editar_inmueble.html'

    def get_success_url(self):
        return reverse_lazy('vista_inmueble', kwargs={'pk': self.object.pk})
    
    def test_func(self):
        inmueble = self.get_object()
        return inmueble.owner == self.request.user  # Solo el propietario puede editar
    
@login_required
def eliminar_inmueble(request, pk):
    inmueble = get_object_or_404(Inmueble, pk=pk)

    if inmueble.owner != request.user:
        messages.error(request, "No tienes permiso para eliminar este inmueble.")
        return redirect('arrendador_account')

    inmueble.delete()  # Elimina el inmueble
    messages.success(request, "El inmueble ha sido eliminado.")
    return redirect('arrendador_account')

    
@login_required
def crear_inmueble(request):
    if request.method == 'POST':
        direccion_form = DireccionForm(request.POST)
        inmueble_form = InmuebleCreationForm(request.POST)
        imagen_form = MultipleImageForm(request.POST, request.FILES)

        if direccion_form.is_valid() and inmueble_form.is_valid() and imagen_form.is_valid():
            direccion = direccion_form.save()
            inmueble = inmueble_form.save(commit=False)
            inmueble.direccion_id = direccion
            inmueble.owner = request.user
            inmueble.save()

            for img in request.FILES.getlist('imagenes'):
                Imagen.objects.create(inmueble=inmueble, imagen=img)

            return redirect('user_redirect')  # Reemplaza con la URL de éxito deseada
    else:
        direccion_form = DireccionForm()
        inmueble_form = InmuebleCreationForm()
        imagen_form = MultipleImageForm()

    return render(request, 'publicar.html', {
        'direccion_form': direccion_form,
        'inmueble_form': inmueble_form,
        'imagen_form': imagen_form,
    })