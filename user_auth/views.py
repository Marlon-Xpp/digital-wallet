from django.shortcuts import render, redirect
from django.contrib import messages
from user_auth.models import CustomUser
from django.contrib.auth.hashers import make_password
import re
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required

from .models import LoginAttempt
from django.utils import timezone
from datetime import timedelta
# Create your views here.
#AQUI VA LA LOGICA  DE LA APLICACION AUTH USER

#FUNCIONALIDADES DEL AUTH_USER
#Registro de usuarios:
#Inicio de sesión y cierre de sesión:
#Bloquear intentos fallidos (nivel de seguridad)
#Restablecimiento de contraseña(opcional)
#Edición de perfil:
#Cambio de contraseña(opcional)
#Seguridad del perfil:




def validate_email(email):
    """Verifica que el correo electrónico tenga un formato válido."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError("El correo electrónico no tiene un formato válido.")

def validate_password(password):
    """Verifica que la contraseña cumpla con ciertos criterios de complejidad."""
    if len(password) < 8:
        raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
    if not re.search(r'\d', password):
        raise ValidationError("La contraseña debe contener al menos un número.")
    if not re.search(r'[A-Z]', password):
        raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")
    if not re.search(r'[a-z]', password):
        raise ValidationError("La contraseña debe contener al menos una letra minúscula.")
    if not re.search(r'[@$!%*?&]', password):
        raise ValidationError("La contraseña debe contener al menos un carácter especial.")
    
    
# cradno una funcion ade validacion para los campos vacios y con n argumentos
def validate_fields(*fields):
    #aplicamos un for para recorrer la tupla y guardr los datos de fields a field 
    for field in fields:
        #aqui verificamos uno x uno el campo field si esta vacio y si fiel no hay nd 
        if not field:
            #si tan solo un campo esta vacio se mostrar el mensaje de error
            print("no puede dejar los campos vacios")
            #se detentra el codigo y mostrar el error con el msj 
            raise ValidationError("no puede dejar los campos vacios")
# para ahcer ocmentario es el sigueinte comando crlt y la tecla arriba de entender 
def signup(request):
    if request.method == "POST":
        #Obtener los datos de entrada y limpiamos los espacios en blaco del incio y del final del texto
        names = request.POST.get("names","").strip()
        lastname = request.POST.get("lastname","").strip()
        username = request.POST.get("username","").strip()
        phone = request.POST.get("phone","").strip()
        email = request.POST.get("email","").strip()
        password = request.POST.get("password","").strip()
        # manejar alguna error que puede suceder dentro del codigo
        try:
            #validar que los campos ingresado por el usaurio no esten vacios
            validate_fields(names, lastname, username, phone, email, password)
            validate_email(email)
            validate_password(password)
            
            #validacion para ver su el username ya es existente
            if CustomUser.objects.filter(username=username).exists():
                #si el usaurio ya existe imprimira el siguiente msj
                print("el username ya existe intenta con otro")
                #aqui detrendra la ejecucion del cdoigo y mostrara el error 
                raise ValidationError("el username ya existe intenta con otro")
            #validacion para ver si el correo ya es existente
            if CustomUser.objects.filter(email=email).exists():
                #si el correo ya existe imprimira el siguiente msj
                print("el correo ya existe intenta con otro")
                #aqui detrendra la ejecucion del cdoigo y mostrara el error 
                raise ValidationError("el correo ya existe intenta con otro")
                
            user = CustomUser(
                first_name = names,
                last_name = lastname,
                username = username,
                email = email,
                phone= phone,
                password = make_password(password) # es mucho mas seguro q usar hash siempre y mas recomndable usar make_password para hacear contraseñas a nivel de seguridad
            )
            #aqui se guardara los datos obtenidos ala base de datos
            user.save()
            #imprimimos un msj de exito
            print("Usuario guardado correctamente.")
            #retornamos y redirigimos a la vista de login
            return redirect("login")
        #capturamos los errores que creamos para q se muestren x aqui
        except ValidationError as e:
            print(f"el error es el siguiente: {e}")
            return render(request, "signup.html", {'error': str(e)} )
        #capturamos un erro general dentro del codigo
        except Exception as e:
            #retornamos y imprimimos el msj de error general dentro del codigo
            print(f"el error es el siguiente: {e}")
            return render(request, "signup.html", {"error": "eror inesperado. profavor intente de nuevo"})
    #retornamos la vista princiapl del signup y lo msotramos 
    return render(request, "signup.html")




MAX_ATTEMPTS = 5  # Número máximo de intentos permitidos
BLOCK_TIME = timedelta(seconds=15)  # Tiempo de bloqueo de 15 segundos se cambiara el tiempo

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        try:
            validate_fields(username, password)
            
            ip_address = request.META.get('REMOTE_ADDR')
            attempts = LoginAttempt.objects.filter(username=username, ip_address=ip_address)
            
            # Verificar si se han superado los intentos permitidos
            if attempts.count() >= MAX_ATTEMPTS:
                last_attempt = attempts.order_by('-timestamp').first()
                if last_attempt and last_attempt.timestamp + BLOCK_TIME > timezone.now():
                    print("Demasiados intentos. Por favor, inténtalo más tarde.")
                    return render(request, "login.html", {"error": "Demasiados intentos. Por favor, inténtalo más tarde."})

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                attempts.delete()# Eliminar registros de intentos fallidos
                auth_login(request, user)
                print("la autentificacion fue exitosa")
                return redirect("index")  # Redirigir a la vista deseada
            else:
                # Registrar el intento fallido
                LoginAttempt.objects.create(username=username, ip_address=ip_address)
                print("La autenticación fue fallida.")
                return render(request, "login.html", {"error": "La autenticación fue fallida."})
            
        except ValidationError as e:
            print(f"el error es : {e}")
            return render(request, "login.html", {"error": str(e)})
        except Exception as e:
            print(f"el error de exception es : {e}")
            return render(request, "login.html", {"error": "Ocurrió un error inesperado."})
    
    # Si es un GET, solo muestra el formulario
    return render(request, "login.html")


#para las funciones snake_case
#para las clases CamelCase o PascalCase
@login_required
def user_profile(request):
    
    return render(request, "user_profile.html")