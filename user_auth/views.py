from django.shortcuts import render
from django.contrib import messages
import re
# Create your views here.
#AQUI VA LA LOGICA  DE LA APLICACION AUTH USER


def Home(reques):
    return render(reques, 'home.html')

def Signup(request):
    
    # logica para el Registro de los usuarios 
    if request.method ==  'POST':
        
        names = request.POST.get("names")
        lastname = request.POST.get("lastname")
        username = request.POST.get("username")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        print(f"""
              Nombres: {names}
              Apellidos: {lastname}
              Username: {username}
              Telefono: {phone}
              Correo: {email}
              Contraseña: {password}
              """)
        
        if len(password) <= 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
            print("la contraseña debe tener al menos 8 caracteres")
            return render(request, 'signup.html')
        else:
            print("la contraseña es mayor a 8 caracteres")
            
        
    return render(request, "signup.html")


def Login(request):
    return render(request, "login.html")
    # logica para el Registro de los usuarios