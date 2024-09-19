from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import re
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
# Create your views here.
#AQUI VA LA LOGICA  DE LA APLICACION AUTH USER

#FUNCIONALIDADES DEL AUTH_USER
#Registro de usuarios:
#Inicio de sesión y cierre de sesión:
#Restablecimiento de contraseña(opcional)
#Edición de perfil:
#Cambio de contraseña(opcional)
#Seguridad del perfil:

def signup(request):
    # Lógica para el registro de usuarios
    if request.method == 'POST':
        names = request.POST.get("names")
        lastname = request.POST.get("lastname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Validar que el usuario no existe ya
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'El nombre de usuario ya existe'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'El correo electrónico ya está registrado'})
        
        # Crear el usuario con contraseña hasheada
        user = User(
            first_name=names.capitalize(),
            last_name=lastname.capitalize(),
            username=username,
            email=email,
            password=make_password(password),  # Hashear la contraseña
        )
        
        # Guardar el usuario en la base de datos
        user.save()

        # Redirigir a la página de inicio o login
        return redirect('login')
    
    # Si es un GET (solo muestra el formulario)
    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        # Obtén los datos del formulario
        username = request.POST.get("username")  # Cambiado a username en lugar de email
        password = request.POST.get("password")

        # Autentica al usuario
        user = authenticate(request, username=username, password=password)  # Cambiado email a username

        if user is not None:
            # Si las credenciales son correctas, inicia la sesión
            auth_login(request, user)
            print("Las credenciales del usuario son correctas")
            return redirect('index')  # Redirige a la página de inicio o donde quieras
        else:
            # Si las credenciales no son correctas, muestra un error
            print('Nombre de usuario o contraseña incorrectos')
            return render(request, "login.html", {'error': 'Nombre de usuario o contraseña incorrectos'})

    # Si es un GET, solo muestra el formulario
    return render(request, "login.html")

    
    
    

#para las funciones snake_case
#para las clases CamelCase o PascalCase
@login_required
def user_profile(request):
    return render(request, "user_profile.html")