from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.tipo_usuario == 'arrendador':
                return redirect('arrendador_dashboard')
            elif user.tipo_usuario == 'arrendatario':
                return redirect('arrendatario_dashboard')
            else:
                return render(request, 'login.html', {'error_message': 'Usuario no reconocido'})
        else:
            return render(request, 'login.html', {'error_message': 'Credenciales incorrectas'})

    return render(request, 'login.html')

# Create your views here.
