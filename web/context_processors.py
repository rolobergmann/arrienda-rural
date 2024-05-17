from web.models import ExtendUsuario, Direccion

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

