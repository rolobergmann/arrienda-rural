from web.models import ExtendUsuario, Direccion, Inmueble

def user_profile_context(request):
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = ExtendUsuario.objects.get(usuario=request.user)
        except ExtendUsuario.DoesNotExist:
            pass  # Handle cases where the user profile might not exist
    return {'user_profile': user_profile}

def direccion_context(request):
    direccion_context = Direccion.objects.get(usuario=request.user)
    return {'direccion': direccion_context}

def arrendatario_context(request):
    arrendatario_context = ExtendUsuario.objects.get(usuario=request.user)
    return {'arrendatario': arrendatario_context}

def inmueble_context(request):
    inmueble_context = Inmueble.objects.get(usuario=request.user)
    for inmueble in inmueble_context:
        inmueble.esta_arrendado = inmueble.estado == False
    return {'inmueble': inmueble_context, 'esta_arrendado': inmueble.esta_arrendado}

