from django.contrib.auth.models import AnonymousUser
from web.models import ExtendUsuario, Direccion, Inmueble

def user_profile_context(request):
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = ExtendUsuario.objects.get(usuario=request.user)
        except ExtendUsuario.DoesNotExist:
            pass  # Handle cases where the user profile might not exist
    return {'user_profile': user_profile}

def user_owner_context(request):
    user = request.user
    if isinstance(user, AnonymousUser):
        return {'is_owner': False}

    # Check if the user owns any properties
    is_owner = Inmueble.objects.filter(owner=user).exists()
    
    return {'is_owner': is_owner}

def user_renter_context(request):
    user = request.user
    if isinstance(user, AnonymousUser):
        return {'is_renter': False}

    # Check if the user is renting any properties
    is_renter = ExtendUsuario.objects.filter(usuario=user, inmuebles_arrendados__isnull=False).exists()

    return {'is_renter': is_renter}

def direccion_context(request):
    if isinstance(request.user, AnonymousUser):
        return {'direccion': None}

    try:
        direccion_context = Direccion.objects.get(usuario=request.user)
    except Direccion.DoesNotExist:
        direccion_context = None

    return {'direccion': direccion_context}

def arrendatario_context(request):
    if isinstance(request.user, AnonymousUser):
        return {'arrendatario': None}

    try:
        arrendatario_context = ExtendUsuario.objects.get(usuario=request.user)
    except ExtendUsuario.DoesNotExist:
        arrendatario_context = None

    return {'arrendatario': arrendatario_context}

def inmueble_context(request):
    if isinstance(request.user, AnonymousUser):
        return {'inmueble': None, 'esta_arrendado': False}

    inmuebles_propietario = Inmueble.objects.filter(owner=request.user)

    # Inicializar la variable fuera del bloque try
    esta_arrendado = False

    try:
        # Verificar si alguno de los inmuebles está arrendado
        esta_arrendado = any(inmueble.estado == False for inmueble in inmuebles_propietario)
    except Exception as e:
        # Capturar cualquier excepción y establecer los valores por defecto
        inmuebles_propietario = None
        esta_arrendado = False
        print(f"Error en inmueble_context: {e}")

    return {'inmueble': inmuebles_propietario, 'esta_arrendado': esta_arrendado}

